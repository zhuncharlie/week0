# Fisetin Profile(D2)

> 查询方式说明:DrugBank 需要登录账号,我没有账号,改用**公开、免登录、可编程访问**的
> PubChem REST API + ChEMBL REST API 做交叉验证,比手动点网页更可重复。
> 所有原始 JSON 响应存档在 `scratchpad/api_raw/`,报告里每条结论都能回溯到查询命令。

## 0. 基本身份(PubChem)

| 字段 | 值 |
|---|---|
| 名称 | Fisetin |
| PubChem CID | [5281614](https://pubchem.ncbi.nlm.nih.gov/compound/5281614) |
| ChEMBL ID | [CHEMBL31574](https://www.ebi.ac.uk/chembl/explore/compound/CHEMBL31574) |
| 分子式 | C15H10O6,MW 286.24 |
| InChIKey | XHEFDIBZLJXQHF-UHFFFAOYSA-N |
| IUPAC 名 | 2-(3,4-dihydroxyphenyl)-3,7-dihydroxychromen-4-one |
| ChEMBL max_phase | 2(曾进入过 II 期临床,非 Fisetin 本身的衰老适应症,是其他适应症如前列腺癌/认知相关的早期试验) |

一句话:Fisetin 是一种**从水果蔬菜里提取出来、口服安全性好的黄酮类小分子**,在"十种黄酮擂台赛"
(Yousefzadeh 2018 Fig.1)里**靠选择性杀衰老细胞的表型胜出**,不是靠对某个蛋白的强结合力胜出。

## 1. 靶点/网络表(按手册 §5 修正后的 schema)

> ⚠️ 这里刻意不用"靶点蛋白"做表头。原因见下面第 2 节的 ChEMBL 实测数据——
> Fisetin 没有一个被实验锁定的主靶点。

| candidate | target_type | target_or_network | evidence_tier | source_url | notes |
|---|---|---|---|---|---|
| Fisetin | phenotypic / SCAPs-network | 抗凋亡存活网络(SCAPs),BCL-2 家族只是**假说候选支**,未被直接结合实验锁定 | 体内+人组织表型实验(Fig.1/3/4/5) | [PDF Fig.1,4](../../../inputs/Fisetin2018.pdf) | 多靶点黄酮,机制未完全解析——这本身是结论,不是我没查全 |
| Fisetin | predicted/promiscuous-binder | ChEMBL 记录到 **117 条**活性数据,覆盖 ~40 个无关靶点(AChE IC50=12nM 最强,其余多在 μM 级),符合黄酮"混杂弱结合剂"特征 | 预测/弱实验(大多是 qHTS 筛选的 Potency,不是确证机制) | [ChEMBL activity API](https://www.ebi.ac.uk/chembl/api/data/activity.json?molecule_chembl_id=CHEMBL31574&pchembl_value__isnull=false) | 这是"黄酮陷阱"的实锤:标签一大把,但大多数靶点跟 senolytic 无关 |
| Fisetin | mechanism (ChEMBL curated) | **0 条**——ChEMBL 的 `mechanism` 端点对 CHEMBL31574 查询返回空 | 无(连"预测"都算不上,是"未定论") | [ChEMBL mechanism API](https://www.ebi.ac.uk/chembl/api/data/mechanism.json?molecule_chembl_id=CHEMBL31574) | 关键发现:业界最权威的药物机制库里,Fisetin **没有一条**被收录的"已验证作用机制"。这比我自己怎么写都更有说服力地证明了手册 §5 的修正是对的 |
| Fisetin | PI3K/AKT/mTOR pathway | 论文正文(Discussion)提到 Fisetin 抑制 PI3K/AKT/mTOR 通路,且团队既往工作显示干扰 PI3K/AKT 可杀衰老细胞 | 文献引用,非本论文直接测定 | 论文 p.9(Discussion, ref [80]) | 跟 Quercetin 报告的 PI3K-delta 机制同一条通路家族,支持"黄酮同源"假说 |
| Fisetin | antioxidant / glutathione pathway | 升高 GSH:GSSG 比值,降低 HNE 加合物 | 实验(本论文 Fig.3F-G, 5L-M) | 论文 Fig.3,5 | 这条机制独立于"杀衰老细胞",可能是 healthspan 延长的**额外贡献因素**而不只是 senolytic 效应——论文自己也承认这点(Discussion 末段) |

## 2. ChEMBL 实测数据怎么支持"没有单一靶点"这个结论

查询 `activity.json?molecule_chembl_id=CHEMBL31574&pchembl_value__isnull=false`,返回 **117 条**
有定量效价(IC50/Ki/Potency)的记录,分散在约 40 个互不相关的靶点上,包括:
乙酰胆碱酯酶(12nM,最强)、线粒体 NADH 氧化酶(15nM)、CDK2/5/6、GSK3、脂氧合酶 ALOX12/15、
多个细胞色素 P450、Caspase-1/7、HIV 整合酶、疟原虫靶点……

**没有一条**是直接针对 BCL-2 或 BCL-xL 的结合实验数据。

这意味着:论文把 Fisetin 归入"BCL-2 家族一支候选"是**基于通路相似性的合理猜测**
(它跟 Dasatinib+Quercetin 搭档打同一类 SCAPs),而不是像 Navitoclax 那样有直接的
蛋白结合常数支撑。我把这个差别标进了上面的证据档位。

## 3. 论文证据卡(按手册 §7 模板)

- 体外:10 黄酮 @5μM,Fisetin 对 SA-β-gal+ 细胞最狠,总细胞相对保全(Fig.1A)
- 人细胞:IMR-90 依托泊苷衰老模型,1–15μM 剂量响应(Fig.1C),约 15μM 时 SA-β-gal+ 细胞掉到约一半以下
- 人组织:脂肪外植块 20μM / 48h,SA-β-gal+ ↓,SASP(IL-6/IL-8/MCP-1)↓(Fig.4E-F, n=3 配对)
- 活体:老年野生鼠 85 周才给药 → 中位 & 最大寿命 ↑(Fig.5A-B)
- 安全性线索:蔬果天然成分,日本人群日摄入量约 0.4mg/天无不良反应报告;高剂量未见不良反应(引言末段引用 [45])

**我因此改主意的地方**:一开始以为"查靶点表"就是去 DrugBank 翻 Fisetin 的 Targets tab、
抄几个蛋白名字下来。查完 ChEMBL 的 117 条活性数据后我意识到——那样做会制造一个
**假精确**的靶点表(好像 Fisetin 真的"打"某几个蛋白一样),但真实情况是它在几十个靶点上
都只有弱到中等的活性,**没有一个强到能解释它的 senolytic 表型**。这是手册 §5 修正的靶点表
schema 在数据层面的印证。

**我仍然不信的地方**:论文把"选择性杀衰老细胞"归因于 SCAPs/BCL-2 家族,但机制部分(Fig.2
之后)实际做的是"测了一堆下游 marker 都下降",**没有一个敲低/敲除 BCL-xL 来验证
必要性的实验**。所以"BCL-2 家族参与"目前更像是"一个合理的候选解释",我在打分的时候
不会把它当成确定的结合机制来用。
