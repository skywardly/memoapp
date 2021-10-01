# メモアプリ

## Cloud Run デプロイ
https://cloud.google.com/python/django/run

### 環境変数
```
export PROJECT_ID=cloud-run-django-tutorial
export PROJECTNUM=200524719768
export REGION=asia-northeast1
export INSTANCE_NAME=memoapp-db
```

### Cloud SQL for MySQL インスタンスを設定する

#### MySQL インスタンスを作成する
```
gcloud sql instances create $INSTANCE_NAME \
    --project $PROJECT_ID \
    --database-version MYSQL_5_7 \
    --tier db-f1-micro \
    --region $REGION
```
#### デフォルト ユーザーを構成する
https://cloud.google.com/sql/docs/mysql/create-manage-users
```
gcloud sql users set-password root \
--host=% \
--instance=$INSTANCE_NAME \
--prompt-for-password
```

#### データベースの作成
```
gcloud sql databases create django-db \
    --instance $INSTANCE_NAME --charset=utf8mb4 --collation=utf8mb4_general_ci
```

#### ユーザーを作成する
https://cloud.google.com/sql/docs/mysql/create-manage-users
```
gcloud sql users create django \
--host=% \
--instance=$INSTANCE_NAME \
--password=django
```

### Cloud Storage バケットを設定する
```
gsutil mb -l asia-northeast1 gs://$PROJECT_ID-media
```

### Secret Manager にシークレット値を保存する
#### Secret Manager シークレットとして Django 環境ファイルを作成する
.env の作成
```
gcloud secrets create django_settings --replication-policy automatic
gcloud secrets versions add django_settings --data-file .env
```

#### サービス アカウント
```
gcloud secrets add-iam-policy-binding django_settings \
    --member serviceAccount:$PROJECTNUM-compute@developer.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
gcloud secrets add-iam-policy-binding django_settings \
    --member serviceAccount:$PROJECTNUM@cloudbuild.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor
```

### Cloud Build に Cloud SQL へのアクセス権を付与する
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$PROJECTNUM@cloudbuild.gserviceaccount.com \
    --role roles/cloudsql.client
```

### データベースマイグレーション
#### Cloud SQL Auth プロキシを起動
```
./cloud_sql_proxy -instances="$PROJECT_ID:$REGION:$INSTANCE_NAME"=tcp:3306
```

#### 別ターミナルでDjangoを実行
```
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
export USE_CLOUD_SQL_AUTH_PROXY=true
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate --settings=memoappproject.settings.prod 
```

### デプロイ
#### Docker イメージビルド
```
gcloud builds submit --config cloudmigrate.yaml
```

#### デプロイ
```
gcloud run deploy memoapp \
    --platform managed \
    --region $REGION \
    --image gcr.io/$PROJECT_ID/memoapp \
    --add-cloudsql-instances $PROJECT_ID:$REGION:$INSTANCE_NAME \
    --allow-unauthenticated
```

### 更新
#### Docker イメージビルド
```
gcloud builds submit --config cloudmigrate.yaml
```

#### デプロイ
```
gcloud run deploy memoapp \
    --platform managed \
    --region $REGION \
    --image gcr.io/$PROJECT_ID/memoapp
```
