import os
from pathlib import Path
from urllib.parse import urljoin

from django.core.files.storage import FileSystemStorage
from environs import Env

env = Env()
env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    ["127.0.0.1", "localhost", "thedevu101.uz", "www.thedevu101.uz"],
)
CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    ["https://thedevu101.uz", "https://www.thedevu101.uz"],
)

# Canonical site info — used to build absolute URLs for SEO / Open Graph.
SITE_DOMAIN = env.str("SITE_DOMAIN", "thedevu101.uz")
SITE_URL = env.str("SITE_URL", "https://thedevu101.uz")

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # modeltranslation must come before admin so it can patch the admin.
    "modeltranslation",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",

    "social_django",
    "django_ckeditor_5",

    # Local apps
    "accounts.apps.AccountsConfig",
    "content.apps.ContentConfig",
    "app_users.apps.AppUsersConfig",
    "app_main.apps.AppMainConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "PROJECT.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "app_main.context_processors.site_meta",
            ],
        },
    },
]

WSGI_APPLICATION = "PROJECT.wsgi.application"

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("PGDATABASE"),
            "HOST": env.str("PGHOST"),
            "PORT": env.str("PGPORT"),
            "USER": env.str("PGUSER"),
            "PASSWORD": env.str("PGPASSWORD"),
        }
    }

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.github.GithubOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Social auth keys (leave blank to disable a provider).
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env.str("GOOGLE_SOCIAL_KEY", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env.str("GOOGLE_SOCIAL_SECRET", "")

SOCIAL_AUTH_GITHUB_KEY = env.str("GITHUB_SOCIAL_KEY", "")
SOCIAL_AUTH_GITHUB_SECRET = env.str("GITHUB_SOCIAL_SECRET", "")

# Send the user back to where they came from after social login.
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/"
SOCIAL_AUTH_JSONFIELD_ENABLED = True

# ---------------------------------------------------------------------------
# Internationalization  (default: Uzbek, no URL prefix; /ru/ and /en/ prefixes)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

_ = lambda s: s  # noqa: E731  (marker only; real translations live in .po files)
LANGUAGES = (
    ("uz", _("O'zbek")),
    ("ru", _("Русский")),
    ("en", _("English")),
)

LOCALE_PATHS = (BASE_DIR / "locale",)

# django-modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = "uz"
MODELTRANSLATION_LANGUAGES = ("uz", "ru", "en")
MODELTRANSLATION_FALLBACK_LANGUAGES = ("uz", "en", "ru")
# CKEditor's rich-text field subclasses TextField but isn't recognised by
# modeltranslation out of the box — whitelist it so bodies can be translated.
MODELTRANSLATION_CUSTOM_FIELDS = ("CKEditor5Field",)

# ---------------------------------------------------------------------------
# Static & media  (served by nginx in production)
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = BASE_DIR / "staticfiles"   # collectstatic target (nginx root)
MEDIA_ROOT = BASE_DIR / "media"          # uploads (nginx root)

STATICFILES_DIRS = [BASE_DIR / "assets"]  # project source assets (tailwind css, js, icons)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Email  (SMTP by default; set EMAIL_BACKEND in the env to override)
# ---------------------------------------------------------------------------
# For local development without SMTP credentials, set in your .env:
#   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# Gmail requires an App Password (not your account password) with 2FA enabled.
EMAIL_BACKEND = env.str(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = env.int("EMAIL_PORT", 587)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", "thedevu101 <no-reply@thedevu101.uz>")

# Recipients notified when a new comment or review is received.
NOTIFY_EMAILS = env.list("NOTIFY_EMAILS", ["thedevu101@gmail.com"])

# ---------------------------------------------------------------------------
# CKEditor 5
# ---------------------------------------------------------------------------
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_FILE_STORAGE = "PROJECT.settings.CustomStorage"
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|", "bold", "italic", "link",
            "bulletedList", "numberedList", "blockQuote", "imageUpload",
        ],
    },
    "extends": {
        "blockToolbar": [
            "paragraph", "heading1", "heading2", "heading3", "|",
            "bulletedList", "numberedList", "|", "blockQuote",
        ],
        "toolbar": [
            "heading", "|", "outdent", "indent", "|", "bold", "italic", "link",
            "underline", "strikethrough", "code", "subscript", "superscript",
            "highlight", "|", "codeBlock", "sourceEditing", "insertImage",
            "bulletedList", "numberedList", "todoList", "|", "blockQuote",
            "imageUpload", "|", "fontSize", "fontFamily", "fontColor",
            "fontBackgroundColor", "mediaEmbed", "removeFormat", "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative", "|", "imageStyle:alignLeft",
                "imageStyle:alignRight", "imageStyle:alignCenter",
                "imageStyle:side", "|",
            ],
            "styles": ["full", "side", "alignLeft", "alignRight", "alignCenter"],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells",
                "tableProperties", "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
            ]
        },
    },
    "list": {
        "properties": {"styles": "true", "startIndex": "true", "reversed": "true"},
    },
}


class CustomStorage(FileSystemStorage):
    """Custom storage for django_ckeditor_5 images."""

    location = os.path.join(MEDIA_ROOT, "django_ckeditor_5")
    base_url = urljoin(MEDIA_URL, "django_ckeditor_5/")
