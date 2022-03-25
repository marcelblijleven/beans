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

## Versioning
Beans uses semantic versioning where the version bumps are based on commit messages.
To create a new release, do the following on the `master` branch:

```bash
make release
```
