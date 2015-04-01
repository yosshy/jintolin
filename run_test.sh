#!/bin/bash

PYTHONPATH=$(dirname $0)

/usr/bin/pep8 .
/usr/bin/nosetests --with-coverage --cover-html --cover-html-dir=/tmp/cover
