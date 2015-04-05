#!/bin/bash

PYTHONPATH=$(dirname $0)

/usr/bin/pep8 .
/usr/bin/nosetests -v --with-coverage --cover-html --cover-html-dir=/tmp/cover
