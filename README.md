Set env variables to configure the DB:
    DB_USER sets db user
    DB_PASS sets db password
    DB_HOST sets db host
    DB_PORT sets db port
    DB_NAME sets db name

use the Makefile to install dependencies and run the app

`make install`: pip install dependencies
`make develop`: run using flask webserver
`make run`: run using tornado webserver
`make migrate`: run alembic migrations

hit /crawl to get the form page, hit /admin instead for the list of all the words
