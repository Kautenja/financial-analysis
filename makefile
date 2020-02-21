# an alias to the python command
PYTHON=python3

# build the LaiNES code, test the Python interface, and build
# the deployment package
all: test deployment

#
# MARK: Development
#

# run the Python test suite
test:
	${PYTHON} -m unittest discover .

#
# MARK: Deployment
#

clean_dist:
	rm -rf build/ dist/ .eggs/ *.egg-info/ || true

clean_python_build:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# clean the build directory
clean: clean_dist clean_python_build

# build the deployment package
deployment: clean
	${PYTHON} setup.py sdist #bdist_wheel

# ship the deployment package to PyPi
ship: test deployment
	twine upload dist/*
