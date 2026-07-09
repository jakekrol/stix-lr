import argparse
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, roc_auc_score


def load_scores_and_labels(path, score_col=0, label_col=1, header=False):
    data = pd.read_csv(
        path,
        sep=None,
        engine="python",
        header=0 if header else None,
        usecols=[score_col, label_col],
    )
    y_score = data.iloc[:, 0].astype(float).to_numpy()
    y_true = data.iloc[:, 1].astype(float).to_numpy()
    return y_score, y_true


def roc_curve_from_scores(y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    return fpr[1:], tpr[1:], thresholds[1:]


def auc_from_scores(y_true, y_score):
    return roc_auc_score(y_true, y_score)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scores', required=True,
                        help='Comma-separated list of score,label TSV files.')
    parser.add_argument('--names',
                        help='Optional comma-separated display names for each file.')
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--title', default='')
    parser.add_argument('--width', type=float, default=6.0)
    parser.add_argument('--height', type=float, default=5.0)
    parser.add_argument('--fontsize', type=float, default=10.0)
    parser.add_argument('--text_fontsize', type=float, default=5.0)
    parser.add_argument('--axis_labelsize', type=float, default=12.0)
    parser.add_argument('--title_fontsize', type=float, default=13.0)
    parser.add_argument('--legend_fontsize', type=float, default=10.0)
    parser.add_argument('--legend_title_fontsize', type=float, default=10.0)
    parser.add_argument('--header', action='store_true')
    parser.add_argument('--score_col', type=int, default=0)
    parser.add_argument('--label_col', type=int, default=1)
    parser.add_argument('--flip', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    return parser.parse_args()

def main():
    args = get_args()

    plt.rcParams.update({"font.size": args.fontsize})

    score_paths = [path.strip() for path in args.scores.split(",") if path.strip()]
    if args.names is not None:
        names = [name.strip() for name in args.names.split(",")]
        if len(names) != len(score_paths):
            raise ValueError(
                f"--names has {len(names)} entries but --scores has {len(score_paths)} files."
            )
    else:
        names = None

    fig, ax = plt.subplots(figsize=(args.width, args.height))

    colors = plt.cm.tab10(np.linspace(0, 1, max(len(score_paths), 1)))
    curves = []

    for idx, score_path in enumerate(score_paths):
        if args.verbose:
            print(f"# score path: {score_path}")
        y_score, y_true = load_scores_and_labels(
            score_path,
            score_col=args.score_col,
            label_col=args.label_col,
            header=args.header,
        )
        y_score = np.asarray(y_score, dtype=float)
        y_true = np.asarray(y_true, dtype=float)
        if args.flip:
            y_score = -y_score

        fpr, tpr, thresholds = roc_curve_from_scores(y_true, y_score)
        auc_value = auc_from_scores(y_true, y_score)
        label = names[idx] if names is not None else os.path.basename(score_path)
        curves.append((auc_value, fpr, tpr, thresholds, label, colors[idx]))

    curves.sort(key=lambda item: item[0], reverse=True)

    all_fpr = []
    all_tpr = []

    for auc_value, fpr, tpr, thresholds, label, color in curves:
        all_fpr.extend(fpr.tolist())
        all_tpr.extend(tpr.tolist())

        j_scores = tpr - fpr
        max_j_index = int(np.argmax(j_scores))
        print(
            f"label={label}",
            f"auROC={auc_value:.3f}",
            f"max_J={j_scores[max_j_index]:.3f}",
            f"threshold={thresholds[max_j_index]}",
            f"TPR={tpr[max_j_index]:.3f}",
            f"FPR={fpr[max_j_index]:.3f}",
            sep='\t',
        )

        ideal_fpr = fpr[max_j_index]
        ideal_tpr = tpr[max_j_index]

        ax.plot(
            fpr,
            tpr,
            label=f"{label} (auROC={auc_value:.3f})",
            color=color,
            lw=1.2,
        )
        ax.plot(
            ideal_fpr,
            ideal_tpr,
            marker='o',
            color=color,
            markersize=4,
            markeredgecolor='black',
            markeredgewidth=0.25,
        )

    ax.set_xlabel("False Positive Rate", fontsize=args.axis_labelsize)
    ax.set_ylabel("True Positive Rate", fontsize=args.axis_labelsize)
    if args.title:
        ax.set_title(args.title, fontsize=args.title_fontsize)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(
        title="Tool & parameter",
        fontsize=args.legend_fontsize,
        title_fontsize=args.legend_title_fontsize,
        loc='lower left',
        frameon=False,
    )

    if all_fpr and all_tpr:
        x_min = min(all_fpr)
        x_max = max(all_fpr)
        y_min = min(all_tpr)
        y_max = max(all_tpr)
        x_pad = max((x_max - x_min) * 0.05, 0.02)
        y_pad = max((y_max - y_min) * 0.05, 0.02)
        ax.set_xlim(max(0.0, x_min - x_pad), min(1.0, x_max + x_pad))
        ax.set_ylim(max(0.0, y_min - y_pad), min(1.0, y_max + y_pad))

    plt.tight_layout()
    plt.savefig(args.output, dpi=300)


if __name__ == '__main__':
    main()

