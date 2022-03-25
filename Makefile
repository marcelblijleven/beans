.PHONY: all install clean_project setup_project release

all: clean_project install

install: ## This will install all required packages
	pip install -r requirements.txt

clean_project: ## This will remove all compiled python, pycache bytecode and egg info
	find . \( -type f -name '*.pyc' -or -type d -name '__pycache__' \) -delete
	find . \( -type d -name '.eggs' -or -type d -name '*.egg-info' -or -type d -name '.pytest_cache' \) | xargs rm -rf

setup_project: ## This will install all required packages and also development tools like pip-tools, pre-commit and git hooks
	pip install -r requirements_dev.txt
	pre-commit install --install-hooks

release:
	chmod +x ./release.sh
	./release.sh
