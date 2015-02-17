all:
	python setup.py build

install:
	python setup.py install


.PHONY: test
test:
	nosetests

list_tests:
	@for i in test/unit/*_test.py; do basename $$i;done | sort

%.py:
	nosetests $@

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
