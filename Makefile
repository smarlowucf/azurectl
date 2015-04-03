version := $(shell python -c 'from azure_cli.version import __VERSION__; print __VERSION__')

pep8:
	tools/run-pep8

all: completion
	python setup.py build

install:
	python setup.py install
	tools/completion_generator > /etc/bash_completion.d/azurectl.sh


.PHONY: test
test:
	nosetests

list_tests:
	@for i in test/unit/*_test.py; do basename $$i;done | sort

%.py:
	nosetests $@

build: pep8 test
	python setup.py sdist
	mv dist/azure_cli-${version}.tar.gz dist/python-azure-cli.tar.gz
	git log | tools/changelog_generator |\
		tools/changelog_descending > dist/python-azure-cli.changes
	cat package/spec-template | sed -e s'@%%VERSION@${version}@' \
		> dist/python-azure-cli.spec
	mkdir -p dist/azure_cli-${version}/completion
	tools/completion_generator \
		> dist/azure_cli-${version}/completion/azurectl.sh
	tar -C dist -czf dist/python-azure-cli-completion.tar.gz \
		azure_cli-${version}
	rm -rf dist/azure_cli-${version}

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
