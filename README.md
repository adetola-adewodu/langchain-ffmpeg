
## Initial Run
1. `python3 -m venv env`
2. `source env/bin/activate`
3. `python -m pip install --upgrade pip`
4. `pip install -r requirements.txt`

## If there is an error installing packages, here are the initial packages:

1. `pip install ffmpeg-python psycopg2-binary sqlalchemy langchain`
2. `pip freeze > requirements.txt`



## Bundle database and app images and run both as containers

    docker compose --file docker-compose.yml up --build -d

## Bring containers down

    docker compose down -v