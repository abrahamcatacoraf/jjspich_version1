# AGENTS.md — JJ SPICH (Taller de Chapa y Pintura)

## Stack

Django 5.2 / Python 3.11 / PostgreSQL / WhiteNoise / ReportLab PDF

## Quick start

```bash
# activate venv first
venv\Scripts\activate
pip install -r requirements.txt
python manage.py crear_grupos       # one-time: creates Administrador, Tecnico, Recepcionista
python manage.py migrate
python manage.py runserver
```

## Commands

| Action | Command |
|---|---|
| Run dev server | `python manage.py runserver` |
| Create groups | `python manage.py crear_grupos` |
| Migrate | `python manage.py migrate` |
| Make migrations | `python manage.py makemigrations` |
| Static deploy | `python manage.py collectstatic --noinput` |
| Tests | `python manage.py test` (all app test files are empty stubs) |

## Architecture

- 5 Django apps: `clientes`, `vehiculos`, `ordenes`, `inventario`, `pagos`
- `taller_jjspich/` — main config, views (dashboard + PDF reports), decorators, custom management commands
- All views are function-based, decorated with `@login_required`
- `perfiles.py` contains group/permission setup logic, called via `crear_grupos` management command
- `decoradores.py` — `solo_admin`, `admin_o_recepcionista` (checks `is_superuser` or group membership)
- PDF generation in `reportes.py` via ReportLab, served as download
- Templates in `templates/` (app-nested subdirs + `base/` for layout)
- Static files in `static/`, collected to `staticfiles/`

## Settings & env

- `.env` has `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DB_*` — loaded via `python-decouple`
- Database: PostgreSQL (via settings, but a `db.sqlite3` file exists on disk — likely stale)
- `LANGUAGE_CODE = 'es-bo'`, `TIME_ZONE = 'America/La_Paz'`

## Role-based access

| Group | Access |
|---|---|
| Administrador | Full (is_staff) |
| Recepcionista | CRUD clientes/vehiculos/ordenes/insumos (no delete) |
| Tecnico | View/edit ordenes only |

## Production

Entrypoint (nixpacks.toml): `python manage.py migrate && gunicorn taller_jjspich.wsgi --log-file -`

## Conventions

- All views use `login_required` at minimum; sensitive views add `solo_admin` or `admin_o_recepcionista`
- Messages use Django's `contrib.messages` framework
- Forms live in each app's `forms.py` (ModelForm pattern)
- `Vehiculo.save()` uppercases `placa` and nulls out irrelevant type field
- Spanish verbose names on all models
