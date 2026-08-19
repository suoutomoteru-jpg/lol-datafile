#!/usr/bin/env python3
"""base_stats / skills / items をまとめて生成し、VERSIONファイルを更新する。"""

import datetime

import generate_base_stats
import generate_items
import generate_skills
from lib import latest_ddragon_version, repo_path


def main():
    version = latest_ddragon_version()
    print(f"DDragon latest version: {version}")

    md = generate_base_stats.build(version)
    with open(repo_path("data", "champions", "base_stats.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print("base_stats.md generated")

    generated, missing = generate_skills.build(version)
    print(f"skills: generated {len(generated)} champions")
    if missing:
        print(f"skills: tooltip未取得のためスキップ ({len(missing)}体): {', '.join(missing)}")

    items_md = generate_items.build(version)
    with open(repo_path("data", "items.md"), "w", encoding="utf-8") as f:
        f.write(items_md)
    print("items.md generated")

    with open(repo_path("VERSION"), "w", encoding="utf-8") as f:
        f.write(f"{version}\n{datetime.datetime.utcnow().isoformat()}Z\n")


if __name__ == "__main__":
    main()
