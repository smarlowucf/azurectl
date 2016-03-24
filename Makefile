version := $(shell python -c 'from azurectl.version import __VERSION__; print __VERSION__')

all:
	python setup.py build
	${MAKE} -C doc/man all

flake8:
	flake8 -v

install:
	python setup.py install
	tools/completion_generator > /etc/bash_completion.d/azurectl.sh
	${MAKE} -C doc/man install

.PHONY: test
test:
	cd test/unit && py.test --no-cov-on-fail --cov=azurectl --cov-report=term-missing --cov-fail-under=100

list_tests:
	@for i in test/unit/*_test.py; do basename $$i;done | sort

%.py:
	cd test/unit && py.test -s $@

build: flake8 test
	${MAKE} -C doc/man all
	# delete version information from setup.py for rpm package
	# we don't want to have this in the egg info because the rpm
	# package should handle package/version requirements
	cat setup.py | sed -e 's@>=[0-9.]*@@g' > setup.build.py
	python setup.build.py sdist
	mv dist/azurectl-${version}.tar.gz dist/python-azurectl-${version}.tar.gz
	rm setup.build.py
	git log | tools/changelog_generator |\
		tools/changelog_descending > dist/python-azurectl.changes
	cat package/spec-template | sed -e s'@%%VERSION@${version}@' \
		> dist/python-azurectl.spec
	mkdir -p dist/azurectl-${version}/completion
	tools/completion_generator \
		> dist/azurectl-${version}/completion/azurectl.sh
	tar -C dist -czf dist/python-azurectl-completion-${version}.tar.gz \
		azurectl-${version}/completion
	mkdir -p dist/azurectl-${version}/doc/man
	cp -a doc/man/*.1.gz dist/azurectl-${version}/doc/man
	tar -C dist -czf dist/python-azurectl-man-${version}.tar.gz \
		azurectl-${version}/doc/man
	rm -rf dist/azurectl-${version}
	${MAKE} -C doc/man clean

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azurectl.egg-info
	rm -rf build
	rm -rf dist
