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
make install
```

After the `make install` command you still need to push the tag to the remote using `git push --follow-tags`.

If you want to make a prerelease, use `cz bump --changelog --prerelease beta` instead.
