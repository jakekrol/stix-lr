#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# stixlr v needlr
files = [
    "hexbin-stixlr_mr1-needlr_ov0.5.png",
    "hexbin-stixlr_mr1-needlr_ov0.7.png",
    "hexbin-stixlr_mr1-needlr_ov0.9.png",
    "hexbin-stixlr_mr5-needlr_ov0.5.png",
    "hexbin-stixlr_mr5-needlr_ov0.7.png",
    "hexbin-stixlr_mr5-needlr_ov0.9.png"
]

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

for ax, f in zip(axes.flat, files):
    img = mpimg.imread(f)
    ax.imshow(img)
    ax.axis("off")

plt.tight_layout()
plt.savefig("combined-hexbin-stixlr-needlr.png", dpi=300, bbox_inches="tight")

# stixlr v svafotate
files = [
    "hexbin-stixlr_mr1-svafotate_ov0.5.png",
    "hexbin-stixlr_mr1-svafotate_ov0.7.png",
    "hexbin-stixlr_mr1-svafotate_ov0.9.png",
    "hexbin-stixlr_mr5-svafotate_ov0.5.png",
    "hexbin-stixlr_mr5-svafotate_ov0.7.png",
    "hexbin-stixlr_mr5-svafotate_ov0.9.png"
]

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

for ax, f in zip(axes.flat, files):
    img = mpimg.imread(f)
    ax.imshow(img)
    ax.axis("off")

plt.tight_layout()
plt.savefig("combined-hexbin-stixlr-svafotate.png", dpi=300)