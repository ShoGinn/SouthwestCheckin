# Makefile for the 'swcheckin' package.

PACKAGE_NAME = swcheckin
PYTHON ?= python3
MAKE := $(MAKE) --no-print-directory
SHELL = bash

default:
	@echo "Makefile for $(PACKAGE_NAME)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make pre-commit   check coding style (PEP-8, PEP-257)'
	@echo '    make test         run the test suite, report coverage'
	@echo '    make docs         update documentation using Sphinx'
	@echo '    make publish      publish changes to GitHub/PyPI'
	@echo '    make clean        cleanup all temporary files'
	@echo

pre-commit: clean
	@TOXENV=pre-commit tox -v


test: clean
	@TOXENV=python tox -v

docs:
	@TOXENV=build-docs tox -v


publish: install
	@git push origin && git push --tags origin
	@$(MAKE) clean
	@pip install --quiet twine wheel
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@$(MAKE) clean

clean:
	@rm -Rf *.egg .cache .coverage .tox build dist docs/build htmlcov coverage.xml .*_cache .eggs
	@find . -d -type d -name __pycache__ -exec rm -Rf {} \;
	@find . -type f -name '*.pyc' -delete

.PHONY: default pre-commit test docs publish clean
