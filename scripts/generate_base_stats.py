#!/usr/bin/env python3
"""DDragon champion.json（ja_JP）からチャンピオン基礎ステータス表を生成する。

出力: data/champions/base_stats.md
"""

import os
import sys

from lib import DDRAGON_API, get_json, latest_ddragon_version, repo_path

STAT_COLUMNS = [
    ("hp", "HP"),
    ("hpperlevel", "HP/Lv"),
    ("hpregen", "HP自然回復"),
    ("hpregenperlevel", "HP自然回復/Lv"),
    ("mp", "MP"),
    ("mpperlevel", "MP/Lv"),
    ("mpregen", "MP自然回復"),
    ("mpregenperlevel", "MP自然回復/Lv"),
    ("attackdamage", "AD"),
    ("attackdamageperlevel", "AD/Lv"),
    ("attackspeed", "AS"),
    ("attackspeedperlevel", "AS成長%/Lv"),
    ("armor", "物理防御"),
    ("armorperlevel", "物理防御/Lv"),
    ("spellblock", "魔法防御"),
    ("spellblockperlevel", "魔法防御/Lv"),
    ("attackrange", "攻撃射程"),
    ("movespeed", "移動速度"),
    ("crit", "クリティカル率"),
    ("critperlevel", "クリティカル率/Lv"),
]


def build(version: str) -> str:
    champ_index = get_json(f"{DDRAGON_API}/cdn/{version}/data/ja_JP/champion.json")
    champions = champ_index["data"]

    lines = []
    lines.append("# チャンピオン基礎ステータス")
    lines.append("")
    lines.append(f"DDragon patch: `{version}`")
    lines.append("")
    lines.append(
        "各値はレベル1時点の基礎値と、レベル毎の成長値（`/Lv`）。"
        "実際のレベルNでの値は概ね `基礎値 + 成長値 × (N-1) × 補正係数` で近似される"
        "（正確な成長曲線は非線形補正が入るため目安）。"
    )
    lines.append("")

    header = ["チャンピオン", "タイトル", "ロール", "リソース"] + [label for _, label in STAT_COLUMNS]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "---|" * len(header))

    for champ_id in sorted(champions.keys()):
        c = champions[champ_id]
        stats = c["stats"]
        row = [
            c["id"],
            c["name"],
            "/".join(c.get("tags", [])),
            c.get("partype") or "-",
        ]
        for key, _ in STAT_COLUMNS:
            row.append(f"{stats.get(key, 0):g}")
        lines.append("| " + " | ".join(str(v) for v in row) + " |")

    return "\n".join(lines) + "\n"


def main(version: str = None):
    if not version:
        version = sys.argv[1] if len(sys.argv) > 1 else latest_ddragon_version()
    md = build(version)
    out_path = repo_path("data", "champions", "base_stats.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"base_stats.md generated (patch {version})")


if __name__ == "__main__":
    main()
