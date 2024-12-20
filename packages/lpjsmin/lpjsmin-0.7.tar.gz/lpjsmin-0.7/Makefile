# Makefile to help automate tasks

PYTHON = python

all: test

.PHONY: test
test:
	tox

.PHONY: dist
dist:
	$(PYTHON) setup . sdist
