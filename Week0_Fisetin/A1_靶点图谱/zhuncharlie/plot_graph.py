"""
把 fisetin_graph.json 的节点+边画成一张图——这是 D5/A1 工位要求的
"Fisetin 的靶点画成小图"。JSON 本身已经是任务书允许的格式("格式随意能读"),
这张图是给人一眼看的版本,数据以 JSON 为准。

节点颜色按 type 分类(8 种类型正好对上8个分类色槽);边的实线/虚线编码
evidence_tier——实验证据画实线,假说/文献引用画虚线。这是整份报告反复强调的
"证据档位"主题在图上的体现,不是随手配色。
"""

import json
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import networkx as nx

_FONT_DIR = os.path.expanduser("~/.fonts")
for _fname in ("NotoSansSC-Regular.ttf", "NotoSansSC-Bold.ttf"):
    _fpath = os.path.join(_FONT_DIR, _fname)
    if os.path.exists(_fpath):
        fm.fontManager.addfont(_fpath)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Noto Sans SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"

# 固定顺序的8分类色槽(来自 dataviz skill 参考色板,顺序即CVD安全性保证,不能打乱)
CATEGORICAL = {
    "molecule":       "#2a78d6",  # blue
    "network":        "#1baf7a",  # aqua
    "protein_family": "#eda100",  # yellow
    "pathway":        "#008300",  # green
    "activity":       "#4a3aa7",  # violet
    "phenotype":      "#e34948",  # red
    "readout":        "#e87ba4",  # magenta
    "molecule_class": "#eb6834",  # orange
}
TYPE_LABEL = {
    "molecule": "分子",
    "network": "网络(SCAPs)",
    "protein_family": "蛋白家族",
    "pathway": "通路",
    "activity": "活性/机制",
    "phenotype": "表型",
    "readout": "实验读数",
    "molecule_class": "药物类别",
}

# 图上展示用的短标签,跟 JSON 里完整的 label 不同只是为了不挤在一起——
# 完整信息(比如PI3K-delta类具体含哪几个药)以 fisetin_graph.json 原文为准。
SHORT_LABEL = {
    "idelalisib_etc": "PI3K-delta抑制剂类",
}


def main():
    with open("fisetin_graph.json") as f:
        data = json.load(f)

    G = nx.DiGraph()
    for n in data["nodes"]:
        G.add_node(n["id"], label=n["label"], type=n["type"])
    for e in data["edges"]:
        is_experimental = e["evidence_tier"].startswith("实验") or e["evidence_tier"].startswith("结构")
        G.add_edge(e["source"], e["target"], solid=is_experimental)

    pos = nx.spring_layout(G, seed=7, k=1.3, iterations=300)

    fig, ax = plt.subplots(figsize=(13, 10), dpi=150)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    node_colors = [CATEGORICAL[G.nodes[n]["type"]] for n in G.nodes]
    node_sizes = [2800 if G.nodes[n]["type"] in ("network", "molecule") and n in ("fisetin", "scaps_network") else 1800 for n in G.nodes]

    solid_edges = [(u, v) for u, v, d in G.edges(data=True) if d["solid"]]
    dashed_edges = [(u, v) for u, v, d in G.edges(data=True) if not d["solid"]]

    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=solid_edges, style="solid",
                            edge_color=INK_MUTED, width=1.4, arrows=True,
                            arrowsize=14, connectionstyle="arc3,rad=0.05", alpha=0.8)
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=dashed_edges, style="dashed",
                            edge_color=INK_MUTED, width=1.1, arrows=True,
                            arrowsize=12, connectionstyle="arc3,rad=0.05", alpha=0.6)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes,
                            edgecolors=SURFACE, linewidths=1.5, alpha=0.95)

    labels = {n: SHORT_LABEL.get(n, G.nodes[n]["label"]) for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=8.3,
                             font_color=INK_PRIMARY, font_family="Noto Sans SC")

    ax.set_title("A1 · Fisetin 靶点/网络图谱", fontsize=15, color=INK_PRIMARY,
                  loc="left", pad=16, fontweight="bold")
    ax.axis("off")

    # 节点类型图例
    from matplotlib.lines import Line2D
    type_handles = [Line2D([0], [0], marker="o", color="none", markerfacecolor=c,
                            markersize=10, label=TYPE_LABEL[t])
                     for t, c in CATEGORICAL.items()]
    edge_handles = [
        Line2D([0], [0], color=INK_MUTED, lw=1.6, linestyle="solid", label="实线 = 实验/计算证据"),
        Line2D([0], [0], color=INK_MUTED, lw=1.4, linestyle="dashed", label="虚线 = 假说/文献引用"),
    ]
    leg1 = ax.legend(handles=type_handles, loc="upper left", bbox_to_anchor=(1.0, 1.0),
                      frameon=False, fontsize=9, title="节点类型", title_fontsize=10,
                      labelcolor=INK_SECONDARY)
    ax.add_artist(leg1)
    ax.legend(handles=edge_handles, loc="lower left", bbox_to_anchor=(1.0, 0.0),
              frameon=False, fontsize=9, title="边的含义", title_fontsize=10,
              labelcolor=INK_SECONDARY)

    fig.text(0.01, 0.01,
              "数据来源:fisetin_graph.json(节点+边,含每条关系的 evidence_tier)",
              fontsize=8, color=INK_MUTED, ha="left")

    fig.tight_layout()
    fig.savefig("fisetin_network.png", facecolor=SURFACE, bbox_inches="tight")
    print("saved fisetin_network.png")


if __name__ == "__main__":
    main()
