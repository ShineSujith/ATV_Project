# ATV_Project

## Setting up a python virtual environment

```bash
python -m venv venv
```

Activate using:

```bash
source venv/Scripts/activate
```

## Installing dependancies

```bash
pip install -r requirements.txt
```

SELF NOTE: run the following commdand when adding new libraries

```bash
pip freeze > requirements.txt
```

set -a && source .env && set +a
python -m uvicorn src.app.microphone_service:app --host localhost --port 8001 --reload
