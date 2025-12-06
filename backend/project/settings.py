import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# ------------------------------
# 環境変数読み込み
# ------------------------------
load_dotenv()  # Docker Compose の env_file を自動で読み込む

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "replace-me-with-secret")
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# 簡易な真偽値パース（環境変数で "1","true","yes" を真とみなす）
def env_bool(name, default=False):
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "on")

# DEBUG の定義（環境変数 DJANGO_DEBUG でコントロール）
DEBUG = env_bool("DJANGO_DEBUG", default=True)  # 開発では True にしておく


def split_and_clean(s):
    return [p.strip() for p in s.split(",") if p.strip()]

# ALLOWED_HOSTS: 環境変数があればそれを優先、なければ開発用の明示的ホストのみ
allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "")
if allowed_hosts_env:
    ALLOWED_HOSTS = split_and_clean(allowed_hosts_env)
else:
    # 開発用デフォルト — 明示的に列挙（絶対に "*" を置かない）
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "backend"]  # 'backend' は docker-compose サービス名で必要

# CORS: ブラウザから来る Origin を列挙する（backend は不要）
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",   # ローカルで Vite
    "http://frontend:3000",    # フロントをコンテナ名で叩く場合
]

# 開発用に別 origin があるなら DEBUG 時に追加する（例: docker 内テスト用）
if DEBUG:
    # もしフロントが別 IP / network address を使うならここに追加
    extra = os.getenv("CORS_EXTRA_ORIGINS", "")
    if extra:
        CORS_ALLOWED_ORIGINS += split_and_clean(extra)

# CSRF: fetch で cookie を使うならこちらも設定（必ずスキーム付き）
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:3000").split(",")
CSRF_TRUSTED_ORIGINS = [u.strip() for u in CSRF_TRUSTED_ORIGINS if u.strip()]


# 優先度: DATABASE_URL > 個別環境変数 > ローカルデフォルト
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=False)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "todo_db"),
            "USER": os.getenv("POSTGRES_USER", "todo_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "kaibasensei"),
            # NOTE: CI では DATABASE_URL を渡すので通常ここは localhost/127.0.0.1 で OK
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": int(os.getenv("POSTGRES_PORT", 5432)),
            "CONN_MAX_AGE": 600,
        }
    }

# ------------------------------
# アプリケーション設定
# ------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    'todo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

# ------------------------------
# REST Framework
# ------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# ------------------------------
# JWT設定
# ------------------------------
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ------------------------------
# 静的ファイル
# ------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
