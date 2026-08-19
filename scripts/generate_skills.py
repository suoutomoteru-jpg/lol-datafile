#!/usr/bin/env python3
"""チャンピオン別スキル数値・説明のMDを生成する。

スキル説明文は、CommunityDragonの生bin形式を自前で再パースするのではなく、
lol-database (nunune.gg) が既に検証済みで生成している解決済みJSON
(frontend/public/tooltips/{ChampionId}.json) を読む。これはnunune.ggの
実行時には一切触れず、GitHub上の静的ファイルを読むだけなので
本番アプリへの影響はない。

出力: data/champions/skills/{ChampionId}.md
"""

import os
import sys

from lib import (
    DDRAGON_API,
    LOL_DATABASE_TOOLTIPS_BASE,
    get_json,
    get_json_or_none,
    latest_ddragon_version,
    repo_path,
    strip_markup,
)

SKILL_ORDER = [("passive", "パッシブ"), ("q", "Q"), ("w", "W"), ("e", "E"), ("r", "R")]


def render_champion_md(champ_id: str, champ_meta: dict, tooltip: dict, version: str) -> str:
    lines = []
    lines.append(f"# {champ_meta['name']}（{champ_meta['title']}）")
    lines.append("")
    lines.append(f"- DDragon ID: `{champ_id}`")
    lines.append(f"- ロール: {'/'.join(champ_meta.get('tags', []))}")
    lines.append(f"- リソース: {champ_meta.get('partype') or 'なし'}")
    lines.append(f"- patch: `{version}`")
    lines.append("")

    skills = tooltip.get("skills", {})
    for key, label in SKILL_ORDER:
        sk = skills.get(key)
        if not sk:
            continue
        lines.append(f"## {label}: {sk.get('name', '?')}")
        lines.append("")
        meta_bits = []
        if sk.get("cooldown"):
            meta_bits.append(f"クールダウン: {sk['cooldown']}")
        if sk.get("cost"):
            meta_bits.append(f"コスト: {sk['cost']}")
        if sk.get("range"):
            meta_bits.append(f"射程: {sk['range']}")
        if sk.get("maxRank"):
            meta_bits.append(f"最大ランク: {sk['maxRank']}")
        if meta_bits:
            lines.append(" / ".join(meta_bits))
            lines.append("")
        lines.append(strip_markup(sk.get("description", "")))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build(version: str):
    champ_index = get_json(f"{DDRAGON_API}/cdn/{version}/data/ja_JP/champion.json")
    champions = champ_index["data"]

    out_dir = repo_path("data", "champions", "skills")
    os.makedirs(out_dir, exist_ok=True)

    generated, missing = [], []
    for champ_id in sorted(champions.keys()):
        tooltip = get_json_or_none(f"{LOL_DATABASE_TOOLTIPS_BASE}/{champ_id}.json")
        if tooltip is None:
            missing.append(champ_id)
            continue
        md = render_champion_md(champ_id, champions[champ_id], tooltip, version)
        with open(os.path.join(out_dir, f"{champ_id}.md"), "w", encoding="utf-8") as f:
            f.write(md)
        generated.append(champ_id)

    return generated, missing


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else None
    if not version:
        version = latest_ddragon_version()
    generated, missing = build(version)
    print(f"skills: generated {len(generated)} champions (patch {version})")
    if missing:
        print(f"skills: tooltip未取得のためスキップ ({len(missing)}体): {', '.join(missing)}")


if __name__ == "__main__":
    main()
