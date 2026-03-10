---
theme: dracula
title: S3 Vectorsの"じゃない"使い方
info: |
  S3 VectorsのRAG以外の活用方法を紹介するライトニングトーク
drawings:
  persist: false
transition: slide-left
---

# S3 Vectorsの"じゃない"使い方

2026/3/11  
JAWS-UG 茨城 #12 春の推しAWSサービスLTまつり！  
raiha(Ryo Aihara) / @raiha_tec

---
layout: two-cols
---

# aws sts get-caller-identity

- **仕事**
    - セキュリティ
    - SOCやログ分析基盤を作ってます
- **趣味**
    - (最近やってないけど)自作スピーカー / 自作キーボード
    - AIエージェントを使ったWebアプリの個人開発
- **好きなAWSサービス**
  <div class="flex gap-4 mt-2 ml-4">
    <div class="flex flex-col items-center">
      <img src="/images/ecs.svg" class="w-12 h-12" />
      <span class="text-sm mt-1">ECS</span>
    </div>
    <div class="flex flex-col items-center">
      <img src="/images/cdk.svg" class="w-12 h-12" />
      <span class="text-sm mt-1">CDK</span>
    </div>
  </div>

::right::

<div class="flex flex-col items-center justify-center h-full">
  <img src="/images/icon.jpg" class="w-64 rounded-lg" />
  <p class="mt-4">𝕏: @raiha_tec</p>
</div>

---
layout: two-cols
---

# S3 Vectorsとは

**AWSのフルマネージドなベクトルストア**

- 2025年7月プレビュー → 2025年12月GA
- ベクトルデータの保存・クエリに特化した専用API
- サーバーレス：インフラのプロビジョニング不要
- S3と同等の耐久性（11 9）・可用性(SLA99.9%)
- 1秒未満のクエリレスポンス
- 最大**20億ベクトル/インデックス**、最大**4,096次元**

::right::

<div class="flex items-center justify-center h-full">
  <img src="/images/s3-vectors.svg" class="w-64 h-64" />
</div>

---
layout: two-cols
---

# S3 Vectorsの構成

```mermaid {scale: 0.65}
graph TD
    VB[(🪣 Vector Bucket<br/>ベクトル専用バケット)]:::s3 --> VI1{{🗂️ Vector Index<br/>インデックスA}}:::index
    VB --> VI2{{🗂️ Vector Index<br/>インデックスB}}:::index
    VI1 --> V1([📍 Vector + Metadata]):::vector
    VI1 --> V2([📍 Vector + Metadata]):::vector
    VI2 --> V3([📍 Vector + Metadata]):::vector

    classDef s3 fill:#3F8624,stroke:#2E6B1A,color:#fff,stroke-width:2px
    classDef index fill:#E07941,stroke:#C4622E,color:#fff,stroke-width:2px
    classDef vector fill:#527FFF,stroke:#3B5FCC,color:#fff,stroke-width:2px
```

::right::

<div class="pl-4 pt-12">

### 3つの主要コンポーネント

- **Vector Bucket** - ベクトル専用の新しいバケットタイプ
- **Vector Index** - ベクトルデータを整理・類似度検索する単位
- **Vector** - 埋め込みベクトル＋メタデータ（タグ、カテゴリ等）

</div>

<div class="absolute bottom-8 left-12 right-12 text-sm opacity-80 flex items-center gap-4">
<Youtube id="soa2HY6_X3o"/>
<div>

 [AI Agent Ready なベクトルストアの最新事情 - S3 Vectors と OpenSearch の使いどころ](https://youtu.be/soa2HY6_X3o?si=HPkKRSqZyFTXEwto)  
 👈オススメです（ギリギリGA前の動画です）

</div>
</div>

---

# S3 Vectorsのメタデータ

ベクトルに付与できる2種類のメタデータ

| | Filterable | Non-filterable |
|---|---|---|
| クエリ時のフィルタリング | ⭕ 可能 | ❌ 不可 |
| サイズ上限 | **2 KB** | **40 KB**(Filterableとの合計) |
| 用途 | カテゴリ、日付等 | 原文テキスト等 |

<div class="flex justify-center">    
```mermaid {scale: 0.85}
graph LR
    Q[🔍 クエリ]:::user -->|類似検索 + フィルタ| S3V[(🪣 S3 Vectors)]:::s3
    S3V -->|Filterable| F[📋 category: ransomware<br/>severity: 9]:::filter
    S3V -->|Non-filterable| NF[📄 原文テキスト<br/>そのまま返却]:::nonfil

    classDef user fill:#527FFF,stroke:#3B5FCC,color:#fff,stroke-width:2px
    classDef s3 fill:#3F8624,stroke:#2E6B1A,color:#fff,stroke-width:2px
    classDef filter fill:#E07941,stroke:#C4622E,color:#fff,stroke-width:2px
    classDef nonfil fill:#545B64,stroke:#3B4045,color:#fff,stroke-width:2px
```
</div>

---

# メタデータフィルタリング

クエリ時にベクトル検索とフィルタ評価を**同時に実行**

<div class="flex gap-6">
<div class="flex-1">

```python
result = s3vectors.query_vectors(
    vectorBucketName="security-news",
    indexName="articles",
    queryVector={"float32": embedding},
    topK=5,
    filter={
        "$and": [
            {"category": {"$eq": "ransomware"}},
            {"severity": {"$gte": 7}},
            {"date": {"$gte": "2026"}}
        ]
    }
)
```

</div>
<div class="flex-1 text-sm">

| 引数 | 説明 |
|------|------|
| `vectorBucketName` | 検索対象のVector Bucket |
| `indexName` | 検索対象のVector Index |
| `queryVector` | 検索クエリのベクトル |
| `topK` | 返却する類似ベクトル数 |
| `filter` | Filterableメタデータの絞り込み条件 |


</div>
</div>

- フィルタは**後処理ではなく検索と並行**して評価
- 演算子: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$exists`, `$and`, `$or`

---

# よくある使い方：RAG

S3 Vectors を使った自前RAGの構成例

```mermaid {scale: 0.75}
graph LR
    Doc[📄 ドキュメント]:::doc -->|Embedding + PutVectors| S3V[(🪣 S3 Vectors)]:::s3
    User[👤 ユーザー]:::user -->|質問をEmbedding<br/>+ QueryVectors| S3V
    S3V -->|類似ドキュメント| LLM[🤖 LLM]:::bedrock
    User -->|質問| LLM
    LLM -->|回答| User

    classDef s3 fill:#3F8624,stroke:#2E6B1A,color:#fff,stroke-width:2px
    classDef bedrock fill:#E07941,stroke:#C4622E,color:#fff,stroke-width:2px
    classDef doc fill:#545B64,stroke:#3B4045,color:#fff,stroke-width:2px
    classDef user fill:#527FFF,stroke:#3B5FCC,color:#fff,stroke-width:2px
```

- **前処理**: ドキュメントをチャンク分割 → Embeddingモデルでベクトル化 → `PutVectors`で保存
- **ランタイム**: 質問をベクトル化 → `QueryVectors`で類似ドキュメント検索 → LLMにコンテキストとして渡し回答生成
- **S3 VectorsのAPIだけ**で安価なRAGが組める

<div class="absolute bottom-12 left-12 right-12 text-xl">

これが王道の使い方。今日は **RAGじゃない使い方** を紹介します！

</div>

---

# "じゃない"使い方① グラフっぽい可視化

S3 Vectorsの**類似度スコア**を関係値として活用する

<div class="flex justify-center">

```mermaid {scale: 0.75}
graph LR
    A([📰 記事A<br/>ランサムウェア攻撃]):::node1 ---|<b>0.92</b>| B([📰 記事B<br/>身代金要求の手口]):::node2
    A ---|<b>0.85</b>| C([📰 記事C<br/>マルウェア解析]):::node3
    B ---|<b>0.88</b>| D([📰 記事D<br/>インシデント対応]):::node4
    B ---|<b>0.76</b>| E([📰 記事E<br/>暗号化手法]):::node5
    C ---|<b>0.81</b>| F([📰 記事F<br/>脆弱性情報]):::node6
    C ---|<b>0.79</b>| G([📰 記事G<br/>ゼロデイ攻撃]):::node7

    classDef node1 fill:#E07941,stroke:#C4622E,color:#fff,stroke-width:2px
    classDef node2 fill:#527FFF,stroke:#3B5FCC,color:#fff,stroke-width:2px
    classDef node3 fill:#DD344C,stroke:#B22A3D,color:#fff,stroke-width:2px
    classDef node4 fill:#3F8624,stroke:#2E6B1A,color:#fff,stroke-width:2px
    classDef node5 fill:#9468BD,stroke:#7550A0,color:#fff,stroke-width:2px
    classDef node6 fill:#545B64,stroke:#3B4045,color:#fff,stroke-width:2px
    classDef node7 fill:#D4A017,stroke:#B8860B,color:#fff,stroke-width:2px

    linkStyle 0 stroke:#E07941,stroke-width:4px
    linkStyle 1 stroke:#DD344C,stroke-width:3px
    linkStyle 2 stroke:#527FFF,stroke-width:3px
    linkStyle 3 stroke:#9468BD,stroke-width:2px
    linkStyle 4 stroke:#545B64,stroke-width:3px
    linkStyle 5 stroke:#D4A017,stroke-width:2px
```

</div>

記事をベクトル化 → QueryVectorsで上位N件＋スコア取得 → **類似度をエッジの重みとしてグラフ構築**

---

# demo

<Youtube id="JiHf-P8qn1M?start=158" class="w-full h-96" />

---

# "じゃない"使い方② タグの自動生成

生成AIのタグ付けの「ブレ」を S3 Vectors で抑制する

**課題**: 生成AIでタグを作ると表記がブレる

| 記事 | 生成AIのタグ |
|------|------------|
| 記事A | `ランサムウェア`, `サイバー攻撃` |
| 記事B | `ランサムウエア`, `サイバーアタック` |
| 記事C | `身代金型ウイルス`, `cyber attack` |

→ 同じ概念なのにタグが統一されない！  
（タグを事前に決めておく方法もあるかもしれないが、**放置していても**問題なく扱えるようにしたい…）

---

# タグ統一の仕組み

```mermaid {scale: 0.75}
graph LR
    AI[🤖 生成AI]:::bedrock -->|新タグ候補| EMB[🔢 Embedding]:::bedrock
    EMB -->|ベクトル化| Q[(🪣 S3 Vectors<br/>QueryVectors)]:::s3
    Q -->|"類似度 > 0.9 ✅"| USE[既存タグを採用]:::reuse
    Q -->|"類似度 < 0.9 🆕"| NEW[新タグとして登録]:::newreg

    classDef bedrock fill:#E07941,stroke:#C4622E,color:#fff,stroke-width:2px
    classDef s3 fill:#3F8624,stroke:#2E6B1A,color:#fff,stroke-width:2px
    classDef reuse fill:#527FFF,stroke:#3B5FCC,color:#fff,stroke-width:2px
    classDef newreg fill:#DD344C,stroke:#B22A3D,color:#fff,stroke-width:2px
```

<div class="flex gap-8">
<div class="flex-1">

1. 生成AIが自由にタグを生成
2. タグをベクトル化してS3 Vectorsにクエリ
3. 類似度が高い → 既存タグを採用
4. 類似タグがない → 新タグとして登録

※既存のタグと新規のタグのどっちを使えばいいのかという考慮は必要かも…

</div>
<div class="flex-1">

```json
{
    "level": "INFO",
    "message": "Tag normalization completed",
    "timestamp": "2026-03-10T07:31:14.438159Z",
    "logger": "AIAnalysisHandler",
    "context": {
        "article_id": "web_20260310073059_6e8bd3d6",
        "new_tags": [
            "Data Sovereignty"
        ],
        "matched_tags": {
            "Cybersecurity": "Cybersecurity",
            "Funding": "Funding"
        }
    }
}
```

</div>
</div>

---

# コスト：S3 Vectorsは安い

1000万ベクトル（1024次元）の場合の月額コスト例（[S3料金ページ 料金の例1](https://aws.amazon.com/jp/s3/pricing/) より）

| 項目 | 単価 | コスト/月 |
|------|------|----------|
| ストレージ（59GB） | $0.06/GB | $3.54 |
| PUT（月16.7%更新） | $0.20/GB | $1.97 |
| クエリ（100万回） | $2.5/百万回 + データ処理 | $5.87 |
| **合計** | | **$11.38** |

**メリット**: サーバーレスで **月額約$11** は安い！

**デメリット**: コールドクエリはサブ秒（数百ms〜1秒）

---

# アプリでのコスト（2週間分）
※現在アプリで取り込んでいる量が**少ない**。かつ、データを**保持し続ける**必要性はあるので、もっとコストはかかるはず。
<div class="flex justify-center">
  <img src="/images/cost.png" class="max-h-96" />
</div>

---
layout: two-cols
---

# 宣伝

今回紹介した内容使ったアプリを **10000 AIdeas Competition** に応募しています！

#### [Threat Lens - AI-Powered Threat Intelligence for IT Teams](https://builder.aws.com/content/39Zwk1hzeRS3kB9phS3GjJOQb1F/aideas-threat-lens-ai-powered-threat-intelligence-for-it-teams)


セミファイナル突破の条件が記事の「いいね」の数です！  
是非お願いします！🙏😭

<div class="flex justify-center mt-4">
  <img src="/images/qr.png" class="w-35" />
</div>

::right::

<div class="flex items-center justify-center h-full">
  <img src="/images/aideas.png" class="max-h-96" />
</div>

---
layout: two-cols
---

# まとめ

- **S3 Vectors** = ベクトルネイティブなサーバーレスストレージ
- 安くベクトルストアを使いたいなら有力な選択肢
- レイテンシが許容できるユースケースに最適
- RAGだけでなく **類似度スコア** を活用した応用が可能
  - **グラフっぽい可視化**: 記事間の関連性をスコアで表現
  - **タグの自動生成**: 生成AIのブレをベクトル類似度で抑制
- ## 「いいね」頼む🙏😭

::right::

<div class="flex items-center justify-center h-full">
  <img src="/images/s3-vectors.svg" class="w-64 h-64" />
</div>
