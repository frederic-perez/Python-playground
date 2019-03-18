# From a bash shell within Windows, you can simply type
#   $ sh run-all-tests.sh
# to run all tests
#
# python -m unittest -v `ls test_*.py | sed 's/.py//'`
python -m unittest `ls test_*.py | sed 's/.py//'`
