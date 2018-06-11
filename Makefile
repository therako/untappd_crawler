.PHONY: develop test coverage clean lint pre-commit upload-package

default: coverage

ci: clean test-setup test-ci lint coverage

develop:
	python setup.py develop
	pip install -r test-requirements.txt
	pip install flake8 restructuredtext_lint
	@echo "#!/bin/bash\nmake pre-commit" > .git/hooks/pre-push
	@chmod a+x .git/hooks/pre-push
	@echo
	@echo "Added pre-push hook! To run manually: make pre-commit"

test-setup:
	pip install -r test-requirements.txt
	pip install -e .

test:
	pip install tox
	tox

test-ci:
	py.test tests

coverage:
	py.test --cov=es2csv_cli tests

coverage-html: coverage clean-coverage-html
	coverage html

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-coverage-html:
	rm -rf htmlcov

clean: clean-pyc clean-build clean-coverage-html

lint-rst:
	pip install restructuredtext_lint
	rst-lint README.rst

lint-pep8:
	pip install flake8
	flake8 es2csv_cli tests

lint: lint-rst lint-pep8

pre-commit: coverage lint

upload-package: lint clean
	pip install twine wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*
