# lol-datafile

League of LegendsのチャンピオンおよびアイテムデータをAIリファレンス用に
Markdownへ整理し、パッチ追従で定期更新するデータリポジトリ。

[nunune.gg](https://github.com/suoutomoteru-jpg/lol-database)（本体アプリ）とは
独立したリポジトリで、生成・更新はnunune.ggの実行時・APIには一切影響しない。

## データ

- `data/champions/base_stats.md` — 全チャンピオンの基礎ステータス・成長値（DDragon由来）
- `data/champions/skills/{ChampionId}.md` — チャンピオン別スキル説明・数値（チャンピオンごとに1ファイル）
- `data/items.md` — 全アイテムの効果・価格（DDragon由来）

## データソース

- 基礎ステータス・アイテム: Riot DDragon（`ja_JP`）から直接取得
- スキル説明文: [lol-database](https://github.com/suoutomoteru-jpg/lol-database)
  （nunune.gg）が生成・コミット済みの解決済みツールチップJSON
  (`frontend/public/tooltips/*.json`) をGitHub上の静的ファイルとして読み取る。
  CommunityDragonの生ゲームデータを再度パースする代わりに、既に検証済みの
  成果物を再利用している。

## 更新

`.github/workflows/update-data.yml` が毎月1日・15日（3:00 JST、LoLのパッチ間隔
に合わせておよそ2週間に1回）に自動実行し、差分があればコミット・pushする。
手動実行は Actions タブから `workflow_dispatch` で可能。

## ローカルでの生成

```
cd scripts
python3 build_all.py
```

標準ライブラリのみで動作（追加の依存インストールは不要）。
