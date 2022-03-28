.PHONY: all install clean_project

all: clean_project install

install: ## This will install all required packages
	pip install -r requirements_dev.txt

clean_project: ## This will remove all compiled python, pycache bytecode and egg info
	find . \( -type f -name '*.pyc' -or -type d -name '__pycache__' \) -delete
	find . \( -type d -name '.eggs' -or -type d -name '*.egg-info' -or -type d -name '.pytest_cache' \) | xargs rm -rf

setup_project: ## This will install pip-tools and pre-commit
	pip install pip-tools

release:
	cz bump --changelog --annotated-tag
	echo "Make sure to push the release using 'git push --follow-tags origin master'"
