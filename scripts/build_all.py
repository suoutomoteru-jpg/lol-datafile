#!/usr/bin/env python3
"""base_stats / skills / items をまとめて生成し、VERSIONファイルを更新する。"""

import datetime
import os

import generate_base_stats
import generate_items
import generate_skills
from lib import latest_ddragon_version, repo_path


def main():
    version = latest_ddragon_version()
    print(f"DDragon latest version: {version}")

    generate_base_stats.main(version)
    generate_skills.main(version)
    generate_items.main(version)

    version_path = repo_path("VERSION")
    os.makedirs(os.path.dirname(version_path), exist_ok=True)
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(f"{version}\n{datetime.datetime.utcnow().isoformat()}Z\n")


if __name__ == "__main__":
    main()
