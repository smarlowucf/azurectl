version := $(shell python -c 'from azure_cli.version import __VERSION__; print __VERSION__')

all:
	python setup.py build
	${MAKE} -C doc/man all

pep8:
	tools/run-pep8

install:
	python setup.py install
	tools/completion_generator > /etc/bash_completion.d/azurectl.sh
	${MAKE} -C doc/man install

.PHONY: test
test:
	nosetests --with-coverage --cover-erase --cover-package=azure_cli --cover-xml
	tools/coverage-check

coverage:
	nosetests --with-coverage --cover-erase --cover-package=azure_cli --cover-xml
	mv test/unit/coverage.xml test/unit/coverage.reference.xml

list_tests:
	@for i in test/unit/*_test.py; do basename $$i;done | sort

%.py:
	nosetests $@

build: pep8 test
	${MAKE} -C doc/man all
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
		azure_cli-${version}/completion
	mkdir -p dist/azure_cli-${version}/doc/man
	cp -a doc/man/*.1.gz dist/azure_cli-${version}/doc/man
	tar -C dist -czf dist/python-azure-cli-man.tar.gz \
		azure_cli-${version}/doc/man
	rm -rf dist/azure_cli-${version}
	${MAKE} -C doc/man clean

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
