# apigateway-lambda-upstash-supabase-app

### 詳細について
- [詳細はこちらの記事で公開しています。](https://qiita.com/eno49conan/items/6d3e98df2ac82613c3b3)

### フォルダ構成の説明
- .github/workflows/sample.yaml
  - pushイベントで使用するworkflowファイル
- db_ddl_data/
  - supabaseに登録するテーブル定義とサンプルデータ
- migrations/
  - alembicの設定ファイルとマイグレーション内容を実装するファイル
- src/
  - FastAPIのアプリケーションファイル
- tests/
  - stepciのworkflowファイル
- .env.sample
  - 必要な環境変数のキーを記載
- Dockerfile
  - FastAPIのアプリケーションをLambda上で動かすための設定
- docker-compose.yaml
  - ローカル開発でアプリとredisとposgresqlを連携したい場合に適宜利用
- pyproject.toml
  - Ruffの設定
- requirements.txt
  - コンテナでのアプリケーション実行に必要なライブラリ一覧

### アプリケーション起動（ローカル環境）
```bash
uvicorn src.main:app --reload
```