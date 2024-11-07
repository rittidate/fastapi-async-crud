# Item CRUD with FastAPI and SQLite

## Run Locally

Clone the project

```bash
$ git clone https://github.com/rittidate/fastapi-item-async-crud.git
```

## How To Run the Server

To run the server, use the following command:

```shell
$ docker compose up
```

This will spin up the server at `http://localhost:8000` with a local SQLite database.

## Api usage examples
To test api, using postman by import `fastapi-item-async-crud.postman_collection.json`


To test api, using openapi by run the server:

```shell
$ docker compose up
```

This will spin up the server and see openapi docs `http://localhost:8000/docs`




## How To Run the Unit Tests
To run the Unit Tests, from the root of the repo run
```shell
$ docker compose run --rm app sh -c "pytest --disable-warnings"
```

You can use `pytest -v` for verbose output and `pytest -s` to disable output capture for better debugging.

## How To Linter the project
To run the Linter, from the root of the repo run
```shell
$ docker compose run --rm app sh -c "flake8"
```