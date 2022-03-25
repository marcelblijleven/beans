# Beans
![beans](https://github.com/marcelblijleven/beans/actions/workflows/tests.yml/badge.svg)

A logging tool for specialty coffee ☕️

## Get started
This will install all required packages for starting the django project.
```bash
make install
```

To run locally for testing, run:
```bash
python manage.py migrate
python manage.py runserver
```

### Get started with development
This will install all required packages, as well as pip-tools, pre-commit and commitizen. It will also
install git hooks in your .git directory.
```bash
make setup_project
```

## Versioning
Beans uses semantic versioning where the version bumps are based on commit messages.

To create a new release, use the following command.

```bash
make release
```

When branch is not equal to master, it will create a beta release.
