#!/usr/bin/env python3
"""DDragon item.json（ja_JP）からアイテム効果一覧のMDを生成する。

説明文はDDragon標準のもので基本置き換えるが、lol-database側で既知の
DDragon記述崩れを手直しした item-desc-fixes.json があれば優先して使う
（こちらも静的ファイル読み取りのみ、nunune.gg本体には影響しない）。

出力: data/items.md
"""

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


def build(version: str) -> str:
    item_index = get_json(f"{DDRAGON_API}/cdn/{version}/data/ja_JP/item.json")
    items = item_index["data"]

    fixes_doc = get_json_or_none(f"{LOL_DATABASE_TOOLTIPS_BASE}/item-desc-fixes.json") or {}
    fixes = fixes_doc.get("fixes", {})

    lines = []
    lines.append("# アイテム効果一覧")
    lines.append("")
    lines.append(f"DDragon patch: `{version}`")
    lines.append("")

    # 購入不可のダミーエントリ（クラス分類用のプレースホルダ等）は除外する
    purchasable = {
        item_id: item for item_id, item in items.items() if item.get("gold", {}).get("purchasable")
    }

    for item_id in sorted(purchasable.keys(), key=lambda i: purchasable[i]["name"]):
        item = purchasable[item_id]
        gold = item.get("gold", {})
        desc_html = fixes.get(item_id) or item.get("description", "")

        lines.append(f"## {item['name']}")
        lines.append("")
        lines.append(
            f"- 価格: {gold.get('total', 0)}G"
            f"（購入: {gold.get('base', 0)}G / 売却: {gold.get('sell', 0)}G）"
        )
        if item.get("tags"):
            lines.append(f"- 分類: {'/'.join(item['tags'])}")
        if item.get("into"):
            into_names = [items[i]["name"] for i in item["into"] if i in items]
            if into_names:
                lines.append(f"- 進化先: {'/'.join(into_names)}")
        lines.append("")
        lines.append(strip_markup(desc_html))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else None
    if not version:
        version = latest_ddragon_version()
    md = build(version)
    with open(repo_path("data", "items.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(f"items.md generated (patch {version})")


if __name__ == "__main__":
    main()
