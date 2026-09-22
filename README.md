# Mocna Drużyna Games Presents - No Name Game

A text-based RPG built with Django and Django REST Framework. Create a hero, explore procedurally generated maps, fight enemies, find loot, and level up — all through a REST API.

## What is this?

Your hero exists on a grid-based map. You move tile by tile, turn left or right, and when something's in front of you, you deal with it. Combat is turn-based and automatic — you hit, they hit back. Find the exit, descend to the next level, repeat. Enemies get stronger. You get stronger. Classic loop.

## Features

- **Hero progression** — XP, levels, base stats that grow
- **Procedural maps** — Walls, empty floors, exits, treasure chests
- **Turn-based combat** — Position matters, direction matters
- **Equipment system** — Weapons, armor, consumables with rarity tiers
- **Inventory management** — Equip/unequip, stat bonuses apply automatically
- **Game log** — Every action recorded, query recent history
- **REST API** — Full CRUD for heroes, map actions, combat, inventory
- **Token auth** — DRF token authentication out of the box

## Tech Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.12+ |
| Framework | Django 6.0 |
| API | Django REST Framework 3.15 |
| Database | SQLite (dev), PostgreSQL (prod) |
| Auth | DRF TokenAuthentication |
| Linting | Ruff |
| Formatting | Black |
| Type checking | mypy + django-stubs |
| Testing | pytest + pytest-django |

## Quick Start

```bash
# clone
git clone https://github.com/yourusername/mocna-druzyna-games.git
cd mocna-druzyna-games

# create venv & install deps
uv venv
source .venv/bin/activate
uv pip install -e .[dev]

# or with pip
python -m venv venv
source venv/bin/activate
pip install -e .[dev]

# migrate & run
python manage.py migrate
python manage.py runserver
```

Server starts at `http://127.0.0.1:8000/`. API at `http://127.0.0.1:8000/api/`.

## Project Structure

```
mocna-druzyna-games/
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── game/                # Main app
│   ├── models.py        # Hero, Map, MapTile, Enemy, Items, GameLog
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # API routes
│   ├── forms.py
│   ├── admin.py
│   └── tests.py
├── manage.py
├── pyproject.toml       # Project config, deps, tooling
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/token/` | Get auth token |
| `GET/POST` | `/api/heroes/` | List/create heroes |
| `GET/PUT/DELETE` | `/api/heroes/{id}/` | Hero detail |
| `POST` | `/api/heroes/{id}/move_forward/` | Move forward |
| `POST` | `/api/heroes/{id}/turn/` | Turn left/right (`{"side": -1}` or `{"side": 1}`) |
| `GET` | `/api/heroes/{id}/visible_tiles/` | Tiles in view cone |
| `GET` | `/api/heroes/{id}/nearby_enemies/` | Enemies in view |
| `GET` | `/api/heroes/{id}/logs/` | Recent game log |
| `GET/POST` | `/api/inventory/` | List/manage inventory |
| `POST` | `/api/inventory/{id}/equip/` | Equip item |

All endpoints require `Authorization: Token <your-token>` header.

## Development

```bash
# lint
ruff check .

# format
black .

# type check
mypy .

# test
pytest

# test with coverage
pytest --cov=game --cov-report=html
```

Pre-commit? Add a `.pre-commit-config.yaml` if you want hooks.

## Configuration

Environment variables (put in `.env` or your shell):

```bash
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3  # or postgres://user:pass@host:5432/db
```

Never commit `SECRET_KEY` or production credentials.

## Deployment Notes

- Set `DEBUG=False`
- Use a real `SECRET_KEY` (generate with `django.core.management.utils.get_random_secret_key()`)
- Switch to PostgreSQL
- Run behind Gunicorn + Nginx
- Serve static files with WhiteNoise or a CDN
- Use a process manager (systemd, supervisor, Docker)
- Set `ALLOWED_HOSTS` to your domain

## License

MIT — do whatever you want, just keep the license notice.

---

Built with ☕ and late-night debugging sessions.