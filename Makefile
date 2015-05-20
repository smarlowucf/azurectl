version := $(shell python -c 'from azurectl.version import __VERSION__; print __VERSION__')

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
	nosetests --with-coverage --cover-erase --cover-package=azurectl --cover-xml
	tools/coverage-check

coverage:
	nosetests --with-coverage --cover-erase --cover-package=azurectl --cover-xml
	mv test/unit/coverage.xml test/unit/coverage.reference.xml

list_tests:
	@for i in test/unit/*_test.py; do basename $$i;done | sort

%.py:
	nosetests $@

build: pep8 test
	${MAKE} -C doc/man all
	# delete version information from setup.py for rpm package
	# we don't want to have this in the egg info because the rpm
	# package should handle package/version requirements
	cat setup.py | sed -e "s@==[0-9.]*'@'@g" > setup.build.py
	python setup.build.py sdist
	rm setup.build.py
	mv dist/azurectl-${version}.tar.gz dist/python-azurectl.tar.gz
	git log | tools/changelog_generator |\
		tools/changelog_descending > dist/python-azurectl.changes
	cat package/spec-template | sed -e s'@%%VERSION@${version}@' \
		> dist/python-azurectl.spec
	mkdir -p dist/azurectl-${version}/completion
	tools/completion_generator \
		> dist/azurectl-${version}/completion/azurectl.sh
	tar -C dist -czf dist/python-azurectl-completion.tar.gz \
		azurectl-${version}/completion
	mkdir -p dist/azurectl-${version}/doc/man
	cp -a doc/man/*.1.gz dist/azurectl-${version}/doc/man
	tar -C dist -czf dist/python-azurectl-man.tar.gz \
		azurectl-${version}/doc/man
	rm -rf dist/azurectl-${version}
	${MAKE} -C doc/man clean

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azurectl.egg-info
	rm -rf build
	rm -rf dist
