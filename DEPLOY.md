# Deployment (Linux + nginx)

## Stack
- Django 5.1, PostgreSQL, gunicorn behind nginx.
- Static & media are served by nginx from `staticfiles/` and `media/`.
- Tailwind is compiled to `assets/css/app.css` (committed) — no Node needed on the server.
- i18n: Uzbek is the default (no URL prefix); Russian and English live under `/ru/` and `/en/`.

## First-time setup
```bash
git clone <repo> /var/www/thedevu101 && cd /var/www/thedevu101
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then edit: SECRET_KEY, DB, social keys, email, NOTIFY_EMAILS

python manage.py migrate
python manage.py createsuperuser
python manage.py compilemessages          # builds locale/**/django.mo from the .po files
python manage.py collectstatic --noinput   # -> staticfiles/ (served by nginx)
```

## Web server
- Copy `deploy/gunicorn.service.sample` to `/etc/systemd/system/thedevu101.service`, then
  `systemctl daemon-reload && systemctl enable --now thedevu101`.
- Copy `deploy/nginx.conf.sample` to `/etc/nginx/sites-available/thedevu101`, symlink into
  `sites-enabled`, adjust `$project` and TLS paths, then `nginx -t && systemctl reload nginx`.
- Issue TLS with certbot: `certbot --nginx -d thedevu101.uz -d www.thedevu101.uz`.

## Rebuilding CSS (only when templates/design change)
```bash
scripts/build_css.sh          # downloads the Tailwind CLI on first run, then compiles + minifies
```

## Updating translations
1. Edit `{% trans %}` / `_()` strings, then `python manage.py makemessages -l uz -l ru -l en`.
2. Translate new entries in `locale/<lang>/LC_MESSAGES/django.po`.
3. `python manage.py compilemessages` and restart gunicorn.
   Post/News **content** (title, body, slug, excerpt) is translated per-language in the admin
   via django-modeltranslation — separate from these UI strings.

## Notes
- Custom user model is `accounts.User` (extends `AbstractUser`).
- New comments/reviews email everyone in `NOTIFY_EMAILS` (sender, content, timestamp).
- Reviews are hidden until `approved = True` in the admin.
