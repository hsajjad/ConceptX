import argparse
import glob
import json
import random

from collections import Counter
from collections import defaultdict, OrderedDict

from pathlib import Path

import jinja2

def gen_table(cluster_counts, clustering, thresholds=[1, 2, 3, 4, 5, 10, 50, 100, 250, 500, 1000], num_sample_clusters=3, num_sample_tokens=3):
    table = []
    all_thresholds = thresholds.copy()
    all_thresholds = [x for x in all_thresholds if x < max(cluster_counts.keys())]
    all_thresholds.append(max(cluster_counts.keys()))
    aggregated_counts = [[] for _ in range(len(all_thresholds))]
    current_bin_idx = 0
    counts = sorted(cluster_counts.keys())
    # table.append(["# Elements", "# Clusters", "Random cluster samples"])

    prev_threshold = 0
    for current_bin_idx, curr_threshold in enumerate(all_thresholds):
        for count in counts:
            if prev_threshold < count <= curr_threshold:
                aggregated_counts[current_bin_idx] += cluster_counts[count]
        all_clusters = aggregated_counts[current_bin_idx]
        sample_clusters = random.sample(all_clusters, k=min(num_sample_clusters, len(all_clusters)))
        sample_clusters = {c_idx: random.sample(list(set(clustering[c_idx])), k=min(num_sample_tokens, len(set(clustering[c_idx])))) for c_idx in sorted(sample_clusters)}
        bucket_str = f"{prev_threshold}-{curr_threshold}"
        prev_threshold = curr_threshold
        table.append([bucket_str, len(aggregated_counts[current_bin_idx]), sample_clusters])

    return table

def decision_fn_max_score(scores):
    return scores.most_common(1)[0]


def decision_fn_ngram(scores):
    scores = [(x, y) for x, y in scores.most_common()]
    threshold_score = 0.95 * scores[0][1]
    scores = [(x, y) for (x, y) in scores if y > threshold_score and len(x) > 1]
    if len(scores) == 0:
        scores = [("_UNK", 0)]
    return max(scores, key=lambda x: len(x[0]))

def casing_preprocess(label):
    if label == "MC":
        return "title_case"
    elif label == "UP":
        return "upper_case"
    else:
        return "lowercase_UNK"

def other_unk_preprocess(label):
    if label == "O":
        return "O_UNK"
    else:
        return label


# Configuration keys:
# 	"ignore": Whether to include this set in the computation
# 	"ignore_unks": If UNKs should be counted as a valid member of the set
# 		when computing overlap. If False, it may give misleading alignments
# 		if a cluster has a large number of UNKs
# 	"decision_fn": How to pick which auto-label to assign to a cluster based
# 		on the choices. Usual choice is decision_fn_max_score, which takes the
# 		max scoring, i.e. in POS, if NN's overlap is 0.95 and VB's overlap is
# 		0.03, NN will be considered.
CONFIGURATION = {
    "Ngrams": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "POS-Coarse": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "FirstWord": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "Casing": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": casing_preprocess,
        "decision_fn": decision_fn_max_score,
    },
    "Prefixes": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "LastWord": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "CCG": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "SEM": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "POS": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "Sports": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "Chunking": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": other_unk_preprocess,
        "decision_fn": decision_fn_max_score,
    },
    "Suffixes": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "Cities": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "NE": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": other_unk_preprocess,
        "decision_fn": decision_fn_max_score,
    },
    "Countries": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "WORDNET": {
        "ignore": False,
        "ignore_unks": True,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "LIWC": {
        "ignore": False,
        "ignore_unks": True,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "bpe": {
        "ignore": True,
        "ignore_unks": True,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "BERT": {
        "ignore": True,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "RoBERTa": {
        "ignore": True,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "XLNet": {
        "ignore": True,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "bert-base-multilingual-cased": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "albert-base-v1": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "xlm-roberta-base": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "bert-base-uncased": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "xlnet-base-cased": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "bert-base-cased": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "roberta-base": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_ngram,
    },
    "brownClusters1000": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "brownClusters800": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "brownClusters600": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "brownClusters50": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
    "__fallback__": {
        "ignore": False,
        "ignore_unks": False,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score,
    },
}


def get_label_set_name(path):
    filename = path.split("/")[-1]

    return filename.split("_")[1][:-5]


def align_autotags(
    clustering, label_set_name, labels, config, threshold=0.9, max_unk_threshold=0.4
):

    alignment_data = defaultdict(list)
    for cluster_idx in clustering:
        for token, sentence_idx, token_idx in clustering[cluster_idx]:
            curr_labels = labels[sentence_idx][token_idx]
            curr_labels = curr_labels.strip().split("|||")
            curr_labels = [config["preprocess_fn"](label) for label in curr_labels]

            alignment_data[cluster_idx].append((token, curr_labels))

    autolabel_to_clusters = defaultdict(dict)
    clusters_to_autolabels_finegrained = defaultdict(dict)
    num_autolabel_aligned_clusters = 0

    for cluster_idx in alignment_data:
        mapping = alignment_data[cluster_idx]
        flattened_mapping = [
            (token, label) for token, labels in mapping for label in labels
        ]

        counts = Counter(flattened_mapping)

        # Count number of unknowns
        unk_count = 0
        for key in counts:
            token, label = key
            if label[-4:] == "_UNK" or label == "N/A":
                unk_count += counts[key]
        if unk_count / len(mapping) > max_unk_threshold:
            # print(f"    Warning: Abandoning cluster {cluster_idx} because of too many UNKs")
            continue

        if config["ignore_unks"]:
            # remove unks
            mapping = [(t, [l for l in ls if l[-4:] != "_UNK"]) for t, ls in mapping]
            # remove tokens with no labels
            mapping = [(t, ls) for t, ls in mapping if ls]
            flattened_mapping = [
                (token, label) for token, labels in mapping for label in labels
            ]
            counts = Counter(flattened_mapping)

        autolabel_counts = Counter()
        for t, l in counts:
            autolabel_counts[l] += counts[(t, l)]

        best_autolabel, best_autolabel_count = config["decision_fn"](autolabel_counts)
        total_count = len(mapping)

        if (
            best_autolabel_count / total_count > threshold
            and "_UNK" not in best_autolabel
        ):
            aligned_tokens = sorted(set([token for token, _ in mapping]))
            autolabel_to_clusters[f"{label_set_name}:{best_autolabel}"][
                cluster_idx
            ] = aligned_tokens
            num_autolabel_aligned_clusters += 1

        filtered_autolabel_counts = {
            f"{label_set_name}:{autolabel}": (autolabel_count / total_count)
            for (autolabel, autolabel_count) in autolabel_counts.items()
            if autolabel_count / total_count > 0.1 and "_UNK" not in autolabel
        }

        if len(filtered_autolabel_counts) <= 6:
            clusters_to_autolabels_finegrained[cluster_idx] = filtered_autolabel_counts

    return (
        autolabel_to_clusters,
        clusters_to_autolabels_finegrained,
        num_autolabel_aligned_clusters,
    )

def load_file(filepath):
    if filepath.endswith(".json"):
        with open(filepath, "r") as file:
            lines = json.load(file)
            lines = [line.split(" ") for line in lines]
    elif filepath.endswith(".txt"):
        with open(filepath, "r") as file:
            lines = file.readlines()
            lines = [line.strip().split(" ") for line in lines]
    return lines


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("labels_filepath", type=str)
    parser.add_argument("sentence_filepath", type=str)
    parser.add_argument("clustering_filepath", type=str)
    parser.add_argument("output_file", type=str)
    parser.add_argument("--ignore_label_indices", type=str, help="Comma separated list of label indices to ignore. ")
    parser.add_argument("-t", "--threshold", type=float, default=0.90)
    parser.add_argument(
        "--max_unk_threshold",
        type=float,
        default=0.4,
        help="If a cluster has more unknowns than that defined by this fraction, it is not assigned any labels",
    )
    parser.add_argument("--save_tokens", action="store_true", default=False)

    parser.add_argument("--ignore_unks", action="store_true", help="Ignore UNKs in alignment computation")
    parser.add_argument("--preprocess_fn", type=str, default="none", help="One of none,casing,other_unk")
    parser.add_argument("--decision_fn", type=str, default="default", help="One of default,ngram")

    args = parser.parse_args()
    print("Loading sentences...")
    sentences = load_file(args.sentence_filepath)

    print("Loading clustering...")
    with open(args.clustering_filepath, "r") as clustering_file:
        clustering = defaultdict(list)
        for sample in clustering_file:
            token, _, sentence_idx, token_idx, cluster_idx = sample.strip().split("|||")
            sentence_idx = int(sentence_idx)
            token_idx = int(token_idx)
            cluster_idx = int(cluster_idx)

            try:
                token = token.encode("ascii").decode("unicode-escape")
            except:
                pass
            stored_token = sentences[sentence_idx][token_idx]

            assert token.encode("utf16", "surrogatepass") == stored_token.encode(
                "utf16", "surrogatepass"
            ), f"WARNING: {token} different than {stored_token} {token} {sample.strip()}"

            clustering[cluster_idx].append((stored_token, sentence_idx, token_idx))

    print("Analyzing Clusters...")
    clusters_by_type_counts = {}
    clusters_by_token_counts = {}
    for cluster_idx in clustering:
        _tokens = [x[0] for x in clustering[cluster_idx]]
        token_count = len(_tokens)
        if token_count not in clusters_by_token_counts:
            clusters_by_token_counts[token_count] = []
        clusters_by_token_counts[token_count].append(cluster_idx)

        type_count = len(set(_tokens))
        if type_count not in clusters_by_type_counts:
            clusters_by_type_counts[type_count] = []
        clusters_by_type_counts[type_count].append(cluster_idx)

    token_to_clusters = {}
    for cluster_idx in clustering:
        for token, _, _ in clustering[cluster_idx]:
            if token not in token_to_clusters:
                token_to_clusters[token] = set()
            token_to_clusters[token].add(cluster_idx)

    token_to_clusters_inv = {}
    for k, v in token_to_clusters.items():
        if len(v) not in token_to_clusters_inv:
            token_to_clusters_inv[len(v)] = []
        token_to_clusters_inv[len(v)].append(k)

    total_tokens = 0
    multiple_cluster_tokens = 0
    duplicated_tokens = {}
    for cluster_count, tokens in sorted(token_to_clusters_inv.items(), key=lambda x: x[0]):
        if cluster_count > 1:
            multiple_cluster_tokens += len(tokens)
            duplicated_tokens[cluster_count] = tokens
        total_tokens += len(tokens)
    duplicate_tagline = f"{multiple_cluster_tokens}/{total_tokens} appear in more than 1 cluster"

    print("Processing labels")
    overall_results = {}
    autolabels_to_clusters_mapping = {}
    clusters_to_autolabels_mapping = defaultdict(list)
    clusters_to_autolabels_finegrained_mapping = defaultdict(list)

    ignore_label_indices = []
    try:
        _l = [int(x) for x in args.ignore_label_indices.split(",")]
        ignore_label_indices = _l
    except:
        pass

    if ignore_label_indices:
        print(f"Warning: Going to ignore following label lines: {ignore_label_indices}")

    config = {
        "ignore_unks": args.ignore_unks,
        "preprocess_fn": lambda x: x,
        "decision_fn": decision_fn_max_score
    }

    print("  Loading...")
    labels = load_file(args.labels_filepath)

    if ignore_label_indices:
        # Delete in reverse order
        for label_line_idx in sorted(ignore_label_indices, key=lambda x: -x):
            del labels[label_line_idx]

    assert len(labels) == len(
        sentences
    ), "Label file is not associated with provided sentences! Mismatch in number of lines"
    # for _ in range(10):
    #     rand_idx = random.randint(0, len(sentences) - 1)
    #     assert len(labels[rand_idx]) == len(
    #         sentences[rand_idx]
    #     ), "Label file is not associated with provided sentences!"
    for idx in range(len(sentences)):
        assert len(labels[idx]) == len(
            sentences[idx]
        ), f"Label file is not associated with provided sentences! Mismatch at {idx}:\n\t{sentences[idx]}\n\t{labels[idx]}"

    print(f"  Aligning...")
    _autolabel_to_clusters, _clusters_to_autolabels_finegrained, _num_autolabel_aligned_clusters = align_autotags(
        clustering,
        "P",
        labels,
        config,
        threshold=args.threshold,
        max_unk_threshold=args.max_unk_threshold,
    )

    label_set = "Propoganda"
    final_label_outputs = {}
    # for tag in _autolabel_to_clusters:
    #     for c in _autolabel_to_clusters[tag]:
    #         if c not in cluster_to_auto_labels:
    #             cluster_to_auto_labels[c] = {}
    #         cluster_to_auto_labels[c][f"{label_set}:{tag}"] = _autolabel_to_clusters[tag][c]

    final_label_outputs[label_set] = {
        "token": {
            "tagline": f"{_num_autolabel_aligned_clusters}/{len(clustering)} clusters are aligned",
            "alignment": _autolabel_to_clusters
        },
        "type": {
            "tagline": f"{_num_autolabel_aligned_clusters}/{len(clustering)} clusters are aligned",
            "alignment": _autolabel_to_clusters
        }
    }

    if args.save_tokens:
        autolabels_to_clusters_mapping.update(_autolabel_to_clusters)
    else:
        autolabels_to_clusters_mapping.update({k:list(v.keys()) for k, v in _autolabel_to_clusters.items()})
    for label in _autolabel_to_clusters:
        for cluster_idx in _autolabel_to_clusters[label]:
            clusters_to_autolabels_mapping[cluster_idx].append(label)
    for cluster_idx in _clusters_to_autolabels_finegrained:
        clusters_to_autolabels_finegrained_mapping[cluster_idx] += sorted([(k, v) for k, v in _clusters_to_autolabels_finegrained[cluster_idx].items()])

    clusters_to_autolabels_mapping_with_tokens = {}
    for label in _autolabel_to_clusters:
        for cluster_idx in _autolabel_to_clusters[label]:
            if cluster_idx not in clusters_to_autolabels_mapping_with_tokens:
                clusters_to_autolabels_mapping_with_tokens[cluster_idx] = {}
            if label not in clusters_to_autolabels_mapping_with_tokens[cluster_idx]:
                clusters_to_autolabels_mapping_with_tokens[cluster_idx][label] = []
            clusters_to_autolabels_mapping_with_tokens[cluster_idx][label] += _autolabel_to_clusters[label][cluster_idx]

    with open(args.output_file, "w") as fp:
        json.dump({
                # "label_sets": label_sets,
                "autolabels_to_clusters_mapping": autolabels_to_clusters_mapping,
                "clusters_to_autolabels_mapping": clusters_to_autolabels_mapping,
                "clusters_to_autolabels_finegrained_mapping": clusters_to_autolabels_finegrained_mapping
            }, fp)

    with open(Path(__file__).parent / "analyze_clustering.html") as template_fp:
        template = jinja2.Template(template_fp.read())
    outputText = template.render(
        clustering_name=args.clustering_filepath,
        token_table=gen_table(clusters_by_token_counts, clustering, num_sample_clusters=10000000, num_sample_tokens=10),
        type_table=gen_table(clusters_by_type_counts, clustering, num_sample_clusters=10000000, num_sample_tokens=10),
        duplicate_tagline=duplicate_tagline,
        duplicated_tokens=duplicated_tokens,
        label_data=final_label_outputs,
        cluster_to_auto_labels=OrderedDict(sorted(clusters_to_autolabels_mapping_with_tokens.items(), key=lambda x: x))
    )  # this is where to put args to the template renderer

    with open(f"{args.output_file}.html", "w") as html_fp:
        html_fp.write(outputText)

if __name__ == "__main__":
    main()
