.PHONY: all install clean_project setup_project release

all: clean_project install

install: ## This will install all required packages
	pip install -r requirements_dev.txt

clean_project: ## This will remove all compiled python, pycache bytecode and egg info
	find . \( -type f -name '*.pyc' -or -type d -name '__pycache__' \) -delete
	find . \( -type d -name '.eggs' -or -type d -name '*.egg-info' -or -type d -name '.pytest_cache' \) | xargs rm -rf

setup_project: ## This will install pip-tools, pre-commit and git hooks
	pip install pip-tools
	pip install pre-commit
	pre-commit install --install-hooks

release:
	BRANCH="$(git rev-parse --abbrev-ref HEAD)"
	if [[ "$BRANCH" != "master" ]]; then
	  echo 'You need to be on the master branch to be able to create a release';
	  exit 1;
	fi

	cz bump --changelog;
