# CLAUDE.md

## Project Overview

LT（ライトニングトーク）用の Slidev プレゼンテーションを管理するリポジトリ。各スライドは `slides/<slide-name>/` ディレクトリに格納される。

## Development Environment

- **devenv**（Nix ベース）で開発環境を管理（`devenv.nix` / `devenv.yaml`）
- `devenv shell` で Node.js / Slidev CLI が利用可能

## Repository Structure

```
slides/<slide-name>/
  slides.md      # メインのスライド（Slidev Markdown）
```

## Common Commands

```bash
# Dev server
cd slides/<slide-name> && npx slidev

# Build
cd slides/<slide-name> && npx slidev build

# Export to PDF
cd slides/<slide-name> && npx slidev export
```

## Slidev Conventions

- `---` でスライドを区切る
- `slides.md` 先頭の frontmatter でテーマ・タイトル等を設定
- LT 向けに簡潔な内容を心がける
- **スライド内の全コンテンツ（テキスト、図、コードブロック等）は必ずスライド内に収まるようにすること。見切れは絶対に避ける。** Mermaid 図は `scale` オプションで縮小する、subgraph の多用を避ける、テキスト量を抑える等で対応する
- スライドは日本語で作成する
- スライドの作成・編集時は `slidev` スキルを利用すること

## Content Research

- スライドの内容は AWS に関するものが多い
- AWS の情報を調べる際は `aws-documentation-mcp-server` の MCP ツール（`search_documentation`, `read_documentation`, `recommend`）または `WebSearch` を使い、最新の情報を取得すること

## Diagrams

- 図が必要な場合は drawio を使用して作成する
- AWS リソースを図示する場合は AWS 公式のリソースアイコンを使用する
