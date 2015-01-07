all:
	python setup.py build

install:
	python setup.py install

tests:
	nosetests

clean:
	find -name *.pyc | xargs rm
	rm -rf azure_cli.egg-info
	rm -rf build
	rm -rf dist
