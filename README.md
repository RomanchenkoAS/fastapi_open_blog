# FastAPI Open blog

## Description

- missing

- Migrations are managed by [Alembic](https://alembic.sqlalchemy.org/en/latest/).

## Requirements

- missing

## Installation

### Install Poetry

- If poetry package manager is not installed, you can install it like this for Windows:

  ```shell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python - <br>
  curl -sSL https://install.python-poetry.org | python -
  ```

- Verify installation

  ```shell
  poetry --version
  ```

- For Linux:

  ```shell
  curl -sSL https://install.python-poetry.org | python3 -
  ```

- Verify installation

  ```shell
  poetry --version
  ```

- Optional step: you can configure poetry to keep all dependencies in the project repository. For that, move into the
  project directory and run:

  ```shell
  poetry config virtualenvs.in-project true
  ```

### Initiate database

- Create Postgre SQL database and user

  ```shell
  sudo -u postgres createuser <username>
  sudo -u postgres createdb openblog_db
  sudo -u postgres psql
  psql=# alter user <username> with encrypted password '<password>';
  psql=# grant all privileges on database <dbname> to <username> ;
  ```

- Create .env file in repository root and fill it like it is shown in .env.example file, for example:

  ```text
  POSTGRES_USER = username
  POSTGRES_PASSWORD = password
  POSTGRES_DB = openblog_db
  POSTGRES_PORT = 5432
  POSTGRES_HOST = localhost
  ```

- Apply alembic migrations to DB

  ```bash
  alembic -c alembic/alembic.ini upgrade head
  ```

- In case of module not found error:

  ```bash
  export PYTHONPATH=$(pwd)
  ```

- or for windows:

  ```shell
  $env:PYTHONPATH = (Get-Location).Path
  ```

- Alternative to alembic is direct creation of tables, append this to main.py:

  ```python
  from db import models
  from db.database_definition import engine
  
  models.Base.metadata.create_all(bind=engine)
  ```