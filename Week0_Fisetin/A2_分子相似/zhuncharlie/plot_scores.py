"""
D4 打分结果的可视化版本。读 scores.tsv(由 similarity.py 生成),画一张排序条形图。

颜色用的是"状态"而不是"类别"——这10个候选不是平等的8类事物,是3种状态:
推荐先验 / 阳性对照或参考(不提名)/ 故意排除的反例。所以用 good/critical 两个
固定状态色 + 一个中性灰,而不是给每个候选随手挑一个颜色(那样会让人误以为
颜色在编码候选身份,其实编码的是"我对它的判断")。
"""

import csv
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

_FONT_DIR = os.path.expanduser("~/.fonts")
for _fname in ("NotoSansSC-Regular.ttf", "NotoSansSC-Bold.ttf"):
    _fpath = os.path.join(_FONT_DIR, _fname)
    if os.path.exists(_fpath):
        fm.fontManager.addfont(_fpath)
plt.rcParams["font.sans-serif"] = ["Noto Sans SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"
STATUS_GOOD = "#0ca30c"
STATUS_CRITICAL = "#d03b3b"
NEUTRAL_FILL = "#dedcd3"
NEUTRAL_EDGE = "#898781"

RECOMMEND = {"Venetoclax"}
EXCLUDE_EXAMPLE = {"Etoposide Phosphate"}  # 故意排除的反例,见 REPORT.md §4


def load_scores(path="scores.tsv"):
    with open(path) as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def status_color(name):
    if name in RECOMMEND:
        return STATUS_GOOD, "推荐先验"
    if name in EXCLUDE_EXAMPLE:
        return STATUS_CRITICAL, "故意排除(反例)"
    return NEUTRAL_FILL, "对照 / 参考,不提名"


def main():
    rows = load_scores()
    rows.sort(key=lambda r: float(r["composite_score"]))  # barh画出来从下到上,升序存,最高分在最上面

    names = [r["candidate"] for r in rows]
    scores = [float(r["composite_score"]) for r in rows]
    colors = []
    edge_colors = []
    seen_labels = {}
    for r in rows:
        c, label = status_color(r["candidate"])
        colors.append(c)
        edge_colors.append(STATUS_GOOD if c == STATUS_GOOD else (STATUS_CRITICAL if c == STATUS_CRITICAL else NEUTRAL_EDGE))
        seen_labels[label] = c

    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    bars = ax.barh(names, scores, color=colors, edgecolor=edge_colors, linewidth=1.2, height=0.62, zorder=3)

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 0.012, bar.get_y() + bar.get_height() / 2,
                f"{score:.3f}", va="center", ha="left", fontsize=9.5, color=INK_PRIMARY)

    ax.set_xlim(0, 0.85)
    ax.set_xlabel("综合分(0–1,越高越优先推荐先验)", fontsize=10, color=INK_SECONDARY)
    ax.set_title("D4 · 候选药综合打分排序", fontsize=13, color=INK_PRIMARY, loc="left", pad=14, fontweight="bold")

    ax.tick_params(axis="y", labelsize=10, colors=INK_PRIMARY, length=0)
    ax.tick_params(axis="x", labelsize=9, colors=INK_MUTED)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(BASELINE)
    ax.xaxis.grid(True, color=GRIDLINE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    # 状态图例(ship with icon+label,不单靠颜色)
    from matplotlib.patches import Patch
    order = ["推荐先验", "对照 / 参考,不提名", "故意排除(反例)"]
    handles = [Patch(facecolor=seen_labels[l], edgecolor=INK_MUTED, label=l) for l in order if l in seen_labels]
    leg = ax.legend(handles=handles, loc="lower right", frameon=False, fontsize=9, labelcolor=INK_SECONDARY)

    fig.text(0.01, -0.02,
              "综合分 = 0.3×结构相似度(Tanimoto) + 0.3×通路重叠 + 0.25×安全性 + 0.15×未验证新鲜度"
              "  ——权重解释见 similarity.py 开头注释 / REPORT.md §4",
              fontsize=8, color=INK_MUTED, ha="left")

    fig.tight_layout()
    fig.savefig("scores_chart.png", facecolor=SURFACE, bbox_inches="tight")
    print("saved scores_chart.png")


if __name__ == "__main__":
    main()
