import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
import argparse
import glob
import numpy as np
# import padding_utils

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--text_fontsize', type=float, default=5.0)
    # padding_utils.add_args(parser)
    return parser.parse_args()

def main():
    args = get_args()

    # results = padding_utils.parse_result_files_by_platform(args.input_path)

    slops=500

    thresholds = np.arange(1, 16)
    
    num_rows = 1
    num_cols = 1
    fig, ax = plt.subplots(num_rows,
                            num_cols,
                            figsize=(args.width, args.height),
                            sharey=True)

    slop_colors = {5:'C0', 10:'C1', 50:'C2', 100:'C3', 500:'C4'}
    

    tps = []
    fps = []

    for j in thresholds:
        tp = len(pos_depths[pos_depths>=j])/len(pos_depths)
        fp = len(neg_depths[neg_depths>=j])/len(neg_depths)
        tps.append(tp)
        fps.append(fp)

        J_scores = [tpr - fpr for tpr, fpr in zip(tps, fps)]
        max_J_index = J_scores.index(max(J_scores))
        print(f'slop={slop}',
                f'seq_type={seq_type}',
                f'max J={J_scores[max_J_index]:.3f}',
                f'threshold={thresholds[max_J_index]}',
                f'TPR={tps[max_J_index]:.3f}',
                f'FPR={fps[max_J_index]:.3f}',
                sep='\t')

        ideal_fpr = fps[max_J_index]
        ideal_tpr = tps[max_J_index]


    ax.plot(fps,
            tps,
            label=f"pad={slop}",
            color=slop_colors[slop],
            lw=1.0)

    ax.plot(ideal_fpr,
            ideal_tpr,
            marker='o',
            color=slop_colors[slop],
            markersize=2,
            markeredgecolor='black',
            markeredgewidth=0.25)
    ax.text(ideal_fpr,
            ideal_tpr,
            f"{thresholds[max_J_index]}",
            fontsize=args.text_fontsize,
            #color=slop_colors[slop],
            color='black',
            horizontalalignment='right',
            verticalalignment='bottom')

    ax.set_ylabel("True Positive Rate", fontsize=args.axis_labelsize)
        # if i == 0:
            # ax.set_ylabel("True Positive Rate", fontsize=args.axis_labelsize)
        # if i == 1:
        #     ax.legend(title="Padding (bp)",
        #               fontsize=args.legend_fontsize,
        #               title_fontsize=args.legend_title_fontsize,
        #               loc='lower right',
        #               frameon=False)
    ax.set_xlabel("False Positive Rate", fontsize=args.axis_labelsize)
    ax.set_title(f"{seq_type.upper()}")
    # padding_utils.format_axis(ax, args)

    x_max = max([ax.get_xlim()[1] for ax in axs])
    for ax in axs:
        ax.set_xlim(0, x_max)

    plt.tight_layout()
    plt.savefig(args.output, dpi=300)


if __name__ == '__main__':
    main()

