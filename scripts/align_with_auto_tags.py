import argparse
import glob
import json
import random

from collections import Counter
from collections import defaultdict


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
            if label[-4:] == "_UNK":
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


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("labels_directory", type=str)
    parser.add_argument("sentence_filepath", type=str)
    parser.add_argument("clustering_filepath", type=str)
    parser.add_argument("output_file", type=str)
    parser.add_argument("ignore_label_indices", type=str, help="Comma separated list of label indices to ignore. ")
    parser.add_argument("-t", "--threshold", type=float, default=0.90)
    parser.add_argument(
        "--max_unk_threshold",
        type=float,
        default=0.4,
        help="If a cluster has more unknowns than that defined by this fraction, it is not assigned any labels",
    )
    parser.add_argument("--save_tokens", action="store_true", default=False)

    args = parser.parse_args()

    label_sets = glob.glob(f"{args.labels_directory}/**/labels_*json", recursive=True)

    print("Loading sentences...")
    with open(args.sentence_filepath, "r") as sentence_file:
        sentences = json.load(sentence_file)
        sentences = [sentence.split(" ") for sentence in sentences]

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

    for label_set in label_sets:
        label_set_name = get_label_set_name(label_set)
        print(f"Found {label_set_name} from {label_set}")
        if label_set_name not in CONFIGURATION:
            print(
                f"  Warning: {label_set_name} configuration not found, using default configuration"
            )
            config = CONFIGURATION["__fallback__"]
        else:
            config = CONFIGURATION[label_set_name]

        if config["ignore"]:
            print(f"  Label set found in ignore list, skipping...")
            continue

        print("  Loading...")
        with open(label_set, "r") as label_file:
            labels = json.load(label_file)
            labels = [label.split(" ") for label in labels]

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
            label_set_name,
            labels,
            config,
            threshold=args.threshold,
            max_unk_threshold=args.max_unk_threshold,
        )

        if args.save_tokens:
            autolabels_to_clusters_mapping.update(_autolabel_to_clusters)
        else:
            autolabels_to_clusters_mapping.update({k:list(v.keys()) for k, v in _autolabel_to_clusters.items()})
        for label in _autolabel_to_clusters:
            for cluster_idx in _autolabel_to_clusters[label]:
                clusters_to_autolabels_mapping[cluster_idx].append(label)
        for cluster_idx in _clusters_to_autolabels_finegrained:
            clusters_to_autolabels_finegrained_mapping[cluster_idx] += sorted([(k, v) for k, v in _clusters_to_autolabels_finegrained[cluster_idx].items()])

    with open(args.output_file, "w") as fp:
        json.dump({
                "label_sets": label_sets,
                "autolabels_to_clusters_mapping": autolabels_to_clusters_mapping,
                "clusters_to_autolabels_mapping": clusters_to_autolabels_mapping,
                "clusters_to_autolabels_finegrained_mapping": clusters_to_autolabels_finegrained_mapping
            }, fp)


        


if __name__ == "__main__":
    main()
