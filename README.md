# Beans
![beans](https://github.com/marcelblijleven/beans/actions/workflows/tests.yml/badge.svg)

A logging tool for specialty coffee ☕️

## Get started
```bash
make install
```

To run locally for testing, run
```bash
python manage.py migrate
python manage.py runserver
```

## Docker
It's possible to run the app with Docker compose, run:

```bash
docker-compose up -d --build
```

Then run the migrations
```bash
docker-compose exec web python manage.py flush --no-input
docker-compose exec web python manage.py migrate
```

(optional, check if the database has the required tables)
```bash
docker-compose exec postgres psql --username={YOUR_USER} --dbname=beans_db
# inside psql:
# \l to list databases
# \c beans_db to see the connection
# \dt to list tables
# \q to quit
```

## Versioning
Beans uses semantic versioning where the version bumps are based on commit messages.
To create a new release, do the following on the `master` branch:

```bash
make install
```

After the `make install` command you still need to push the tag to the remote using `git push --follow-tags`.

If you want to make a prerelease, use `cz bump --changelog --prerelease beta` instead.
