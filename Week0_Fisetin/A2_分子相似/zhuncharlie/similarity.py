"""
D4 · 我自己的打分方法

目的:candidate_table.tsv 里的 10 个候选药,谁"长得像 Fisetin"、谁"该先验"?

方法(诚实写清楚,土也没关系):
1. 结构相似度:Morgan 指纹(半径2,2048位)算 Tanimoto 相似度,跟 Fisetin 比。
   —— 这是"像不像"的量化版,但论文已经明确说 Fisetin 是表型/网络级 senolytic,
      不是靠结构直接推 senolytic 活性,所以这一项我只给 30% 权重,不能当成唯一标准。
2. 通路重叠粗打分(0/1/2 人工标注,依据 candidate_table 的 target_or_network 列):
   0 = 机制类别完全不同,1 = 同通路家族,2 = 直接同网络假说(SCAPs/BCL-2)
3. 安全性粗打分(0/1/2,依据 candidate_table 的 safety_note/black_box_warning):
   0 = 有black box warning或已知严重毒性,1 = 轻度安全性问题,2 = 无black box警告
4. "未验证新鲜度"粗打分(0/1,人工标注):
   1 = 我在这次查询范围内没找到它被直接测过senolytic活性的证据,0 = 已经被充分研究过

最终分 = 0.3*结构相似度(归一化到0-1) + 0.3*(通路/2) + 0.25*(安全/2) + 0.15*未验证新鲜度

这个权重是我自己定的,偏见来源写在 REPORT.md 里:我故意把"结构相似度"压到 30%权重,
因为论文核心教训就是"长得像不代表是senolytic"——如果给结构相似度更高权重,
这个分数会系统性地偏向"像黄酮的分子",而忽略真正支撑senolytic假说的是通路证据和安全窗口。
"""

from rdkit import Chem
from rdkit.Chem import DataStructs
from rdkit.Chem import rdFingerprintGenerator
import csv
import json

_morgan_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)

# 结构数据只有一份来源:real_smiles.json(直接从 ChEMBL molecule API 抓的,不手敲)。
# 第一版我手敲过几个复杂结构(Navitoclax/Venetoclax等),跟真实骨架对不上——
# 这是我自己在D4踩的一个坑:复杂药物分子的SMILES千万别凭记忆默写,所以这版改成
# 脚本直接读抓取结果,杜绝二次抄错的可能。real_smiles.json 的抓取过程见
# ../../C_数据地基/run.sh 同款查询逻辑。
with open("real_smiles.json") as f:
    _SMILES = json.load(f)

FISETIN_SMILES = _SMILES["Fisetin"]

# 通路重叠 / 安全性 / 新鲜度是人工判断,来源见 candidate_table.tsv 对应行,
# 这里的 key 要和 real_smiles.json 对应(Etoposide Phosphate 是 ChEMBL 里的实际制剂名)。
MANUAL_SCORES = {
    # name: (pathway_score 0/1/2, safety_score 0/1/2, novelty_score 0/1)
    "Quercetin":            (2, 1, 0),
    "Dasatinib":             (0, 1, 0),
    "Navitoclax":            (2, 0, 0),
    "Venetoclax":            (2, 2, 1),
    "Idelalisib":            (1, 0, 1),
    "Duvelisib":             (1, 0, 1),
    "Copanlisib":            (1, 1, 1),
    "Sirolimus":             (1, 0, 0),
    "Everolimus":            (1, 0, 0),
    "Etoposide Phosphate":   (1, 2, 0),  # pathway=1: TOP2抑制机制重叠,但方向相反(故意纳入做对照,见REPORT.md §4)
}

def tanimoto(smiles_a, smiles_b):
    mol_a = Chem.MolFromSmiles(smiles_a)
    mol_b = Chem.MolFromSmiles(smiles_b)
    fp_a = _morgan_gen.GetFingerprint(mol_a)
    fp_b = _morgan_gen.GetFingerprint(mol_b)
    return DataStructs.TanimotoSimilarity(fp_a, fp_b)

def main():
    rows = []
    for name, (pathway, safety, novelty) in MANUAL_SCORES.items():
        smiles = _SMILES[name]
        try:
            sim = tanimoto(FISETIN_SMILES, smiles)
        except Exception as e:
            print(f"SMILES解析失败 {name}: {e}")
            sim = 0.0
        score = 0.3 * sim + 0.3 * (pathway / 2) + 0.25 * (safety / 2) + 0.15 * novelty
        rows.append((name, round(sim, 3), pathway, safety, novelty, round(score, 3)))

    rows.sort(key=lambda r: -r[5])

    print(f"{'候选':14s} {'结构相似度':10s} {'通路分':6s} {'安全分':6s} {'新鲜度':6s} {'综合分':8s}")
    for r in rows:
        print(f"{r[0]:14s} {r[1]:<10} {r[2]:<6} {r[3]:<6} {r[4]:<6} {r[5]:<8}")

    with open("scores.tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["candidate","tanimoto_to_fisetin","pathway_score_0to2","safety_score_0to2","novelty_0or1","composite_score"])
        for r in rows:
            w.writerow(r)

if __name__ == "__main__":
    main()
