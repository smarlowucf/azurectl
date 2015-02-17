all:
	python setup.py build

install:
	python setup.py install


.PHONY: test
test:
	nosetests

clean:
	find -name *.pyc | xargs rm -f
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
