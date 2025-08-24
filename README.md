Requirements: Python 3,13

instal gcc 11, brew install

`brew install gcc@11`

Instal mysql pkg-config:

`brew install mysql pkg-config`

Setup:

`make setup`

Create table:

`alembic revision -m "create persons table"`

execute migrations:
`alembic upgrade head`

connect database:
mysql -u localadmin -p -h 127.0.0.1 -P 3306 medical_record

SELECT \* FROM person LIMIT 10;
