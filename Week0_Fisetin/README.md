# Week0_Fisetin —— 交付物工作台

> 本目录是 `inputs/Week0_任务交代与完成标准.md` §8 要求的工作台。
> 本轮**solo 完成,一人覆盖 A1/A2/B/C/D 多个工位**(任务书假设多人分工,
> D5 没有强制工位划分,我按自己判断补齐了最有价值的几块,见根 README 的说明)。

## 30 秒读完:结论是什么

Fisetin 不是单靶点药,是在"10 种黄酮擂台赛"里**靠选择性杀衰老细胞的表型**胜出的黄酮
(论文已证,ChEMBL 实测佐证:它没有一条 curated 机制记录,却在 ~40 个无关靶点上有弱活性)。
从它被假设压制的 SCAPs/BCL-2 家族网络出发,在已上市药里筛出 10 个候选,
**排序第一推荐先验的是 Venetoclax**(2016年上市的BCL-2选择性抑制剂)——
比教科书级的 Navitoclax 更安全(不打BCL-xL),且没查到它被直接测过对衰老细胞的清除效果。

## 给审阅者的推荐阅读顺序(按优先级,预计 10–15 分钟读完全部)

| 顺序 | 文件 | 对应任务书要求 | 预计耗时 |
|---|---|---|---|
| 1 | [`A1_靶点图谱/zhuncharlie/REPORT.md`](A1_靶点图谱/zhuncharlie/REPORT.md) | §8① 主报告(★从这里开始) | 5 min |
| 2 | [`candidate_table.tsv`](candidate_table.tsv) | §8③ 全组共用候选药表 | 2 min |
| 3 | [`B_临床话术/elevator_pitch.md`](B_临床话术/elevator_pitch.md) | §8④ 30秒电梯陈述 | 1 min |
| 4 | [`A1_靶点图谱/zhuncharlie/fisetin_profile.md`](A1_靶点图谱/zhuncharlie/fisetin_profile.md) | §7 A1 工位文件,REPORT.md 里每条结论的详细出处 | 3 min |
| 5(可选) | [`A2_分子相似/zhuncharlie/similarity.py`](A2_分子相似/zhuncharlie/similarity.py) + `scores.tsv` | §7 A2 工位文件,REPORT §4 打分方法的可运行版本 | 2 min |
| 6(可选) | [`B_临床话术/assay_plan.md`](B_临床话术/assay_plan.md) | 具体验法,给合作医生看的版本 | 2 min |
| 7(可选) | [`A1_靶点图谱/zhuncharlie/fisetin_graph.json`](A1_靶点图谱/zhuncharlie/fisetin_graph.json) | §7 A1 靶点/网络图(节点+边) | — |
| 8(可选) | [`D_生物翻译/concept_cards.md`](D_生物翻译/concept_cards.md) | §7 D 工位,5个概念卡 | 2 min |
| 9(可选) | [`C_数据地基/dataset.yaml`](C_数据地基/dataset.yaml) + [`run.sh`](C_数据地基/run.sh) | §7 C 工位,数据可复现性 | — |
| 背景 | [`A1_靶点图谱/zhuncharlie/notes.md`](A1_靶点图谱/zhuncharlie/notes.md) | D1 草稿碎片,5个核心词自己的定义 | — |

## 目录结构

```text
Week0_Fisetin/
├── README.md                          本文件(导览)
├── candidate_table.tsv                全组共用候选药表,10行(含3个必填对照行)
├── A1_靶点图谱/zhuncharlie/
│   ├── REPORT.md                      ★主报告,先看这个
│   ├── fisetin_profile.md             Fisetin档案(按手册修正后的schema)
│   ├── fisetin_graph.json             靶点/网络图谱(节点+边)
│   └── notes.md                       D1草稿:5个核心词自己的定义
├── A2_分子相似/zhuncharlie/
│   ├── similarity.py                  D4打分脚本(Tanimoto+通路+安全+新鲜度)
│   ├── real_smiles.json               候选药SMILES(唯一结构数据源,脚本实际读取)
│   └── scores.tsv                     脚本运行输出
├── B_临床话术/
│   ├── elevator_pitch.md              30秒电梯陈述
│   └── assay_plan.md                  具体验法(给合作医生看)
├── C_数据地基/
│   ├── dataset.yaml                   数据集/依赖/复现步骤说明
│   ├── run.sh                         一键重新拉取API数据(已验证可跑)
│   └── raw_cache/                     报告里每条结论对应的原始API JSON(已提交,不在/tmp)
└── D_生物翻译/
    └── concept_cards.md               5张概念卡(给看不懂生物的人)
```

## 为什么是这个结构

- 完全照 `inputs/Week0_任务交代与完成标准.md` 附录A的工位划分来,没有自创目录。
- 每个工位文件夹下按"谁做的"再分一层子目录(`zhuncharlie/`),跟任务书给的示例
  (`A1_靶点图谱/zhangsan/`)一致,即使只有一人也保留这层,方便以后其他人并行往同一工位加东西。
- `raw_cache/` 是这次整理新加的:之前原始 API 响应只存在本机临时目录,仓库里的引用是空链接,
  审阅者点不开。现在把每条**被报告实际引用**的原始数据搬进仓库,探索性但没用上的查询
  (比如 DrugAge 的 404 页面、PubChem PUG View 里没读到的章节)没有收进来,避免堆废数据。
