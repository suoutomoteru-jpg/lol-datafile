"""共通ユーティリティ: HTTP取得・DDragonバージョン解決・タグ除去。

依存は標準ライブラリのみ（lol-databaseの既存スクリプトと同じ方針）。
"""

import json
import os
import re
import urllib.error
import urllib.request

UA = {"User-Agent": "lol-datafile-generator/1.0"}

# 実行時のカレントディレクトリに依存せず、常にリポジトリルート基準で
# 出力先を解決する（`python3 scripts/build_all.py` / `cd scripts && python3 build_all.py`
# のどちらで呼んでも同じ場所に書き出すため）
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def repo_path(*parts: str) -> str:
    return os.path.join(REPO_ROOT, *parts)

DDRAGON_API = "https://ddragon.leagueoflegends.com"
# lol-database (nunune.gg) が生成・コミットしている、CommunityDragonのLCUツールチップを
# 解決済みの日本語スキル説明文JSON。生のCommunityDragon bin形式を再度パースする代わりに、
# 既に検証済みのこの成果物を読む（別リポジトリの静的ファイル読み取りのみで、
# nunune.ggの実行時・APIには一切触れない）。
LOL_DATABASE_TOOLTIPS_BASE = (
    "https://raw.githubusercontent.com/suoutomoteru-jpg/lol-database/main/frontend/public/tooltips"
)


def get_bytes(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read()


def get_json(url: str, timeout: int = 60):
    return json.loads(get_bytes(url, timeout))


def get_json_or_none(url: str, timeout: int = 60):
    """404等は None を返す（一部チャンピオンのツールチップ未生成などに対応）"""
    try:
        return get_json(url, timeout)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def latest_ddragon_version() -> str:
    versions = get_json(f"{DDRAGON_API}/api/versions.json")
    return versions[0]


def strip_markup(s: str) -> str:
    """DDragon/CommunityDragon由来のHTML風タグを除去して平文化する"""
    if not s:
        return ""
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<li>", "\n・", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()
