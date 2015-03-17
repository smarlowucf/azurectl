version := $(shell python -c 'from azure_cli.version import __version__; print __version__')

.PHONY: completion
completion:
	./.completion_metadata > completion/azure-cli.sh

all: completion
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

build: test completion
	python setup.py sdist
	mv dist/azure_cli-${version}.tar.gz dist/python-azure-cli.tar.gz
	git log | ./.changelog | ./.descending > dist/python-azure-cli.changes
	cat ./.spec-template | sed -e s'@%%VERSION@${version}@' \
		> dist/python-azure-cli.spec
	mkdir dist/azure_cli-${version}
	cp -a completion dist/azure_cli-${version}
	tar -C dist -czf dist/python-azure-cli-completion.tar.gz \
		azure_cli-${version}
	rm -rf dist/azure_cli-${version}

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
