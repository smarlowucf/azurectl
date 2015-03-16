version := $(shell python -c 'from azure_cli.version import __version__; print __version__')

all:
	python setup.py build

install:
	python setup.py install
	cp completion/azure-cli.sh /etc/bash_completion.d


.PHONY: test
test:
	nosetests

list_tests:
	@for i in test/unit/*_test.py; do basename $$i;done | sort

%.py:
	nosetests $@

build:
	python setup.py sdist
	git log | ./.changelog > dist/azure-cli.changes
	cat ./.spec-template | sed -e s'@%%VERSION@${version}@' > dist/azure-cli.spec

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
