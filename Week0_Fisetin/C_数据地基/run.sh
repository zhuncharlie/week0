#!/usr/bin/env bash
# C 岗 run.sh —— 换台机器一键重跑数据拉取部分(需要网络 + python3 + requests)
# 用法: bash run.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/../../scratchpad_rerun"
mkdir -p "$OUT_DIR"

echo "[1/2] 检查依赖..."
python3 -c "import requests" 2>/dev/null || { echo "缺 requests: pip install requests"; exit 1; }

echo "[2/2] 拉取 Fisetin 基础数据 (PubChem + ChEMBL)..."
python3 - "$OUT_DIR" << 'EOF'
import sys, json, requests

out_dir = sys.argv[1]

# PubChem: Fisetin 基本属性
r = requests.get(
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/fisetin/property/"
    "CanonicalSMILES,MolecularFormula,MolecularWeight,InChIKey/JSON",
    timeout=15,
)
r.raise_for_status()
with open(f"{out_dir}/pubchem_fisetin_props.json", "w") as f:
    json.dump(r.json(), f, indent=2)
print("  PubChem OK:", r.json()["PropertyTable"]["Properties"][0]["CID"])

# ChEMBL: Fisetin 分子记录 + mechanism(验证"无curated机制"这个关键结论仍然成立)
r2 = requests.get(
    "https://www.ebi.ac.uk/chembl/api/data/molecule.json",
    params={"pref_name__iexact": "FISETIN"},
    timeout=15,
)
r2.raise_for_status()
mol_id = r2.json()["molecules"][0]["molecule_chembl_id"]
with open(f"{out_dir}/chembl_fisetin_molecule.json", "w") as f:
    json.dump(r2.json(), f, indent=2)

r3 = requests.get(
    "https://www.ebi.ac.uk/chembl/api/data/mechanism.json",
    params={"molecule_chembl_id": mol_id},
    timeout=15,
)
r3.raise_for_status()
n_mech = r3.json()["page_meta"]["total_count"]
print(f"  ChEMBL OK: {mol_id}, curated mechanisms = {n_mech} (报告里断言的是 0)")

print("完成。原始 JSON 存在:", out_dir)
EOF

echo "若要重新生成相似度打分表,运行:"
echo "  cd ../A2_分子相似/zhuncharlie && python3 similarity.py"
