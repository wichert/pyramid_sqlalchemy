Reporting an issue
------------------

When submitting a ticket please include the following information:

* the installed version of `pyramid_sqlalchemy`
* the installed version of `pyramid`
* the installed version of `SQLAlchemy`
* if you encounter an exception: the complete Python backtrace


Patches and pull requests
-------------------------

When submitting a patch or pull request please make sure it applies cleanly to
the current git master branch and all tests are passing on Python 2.7 and
Python 3.4. To easiest way to run the tests is to use pytest in a virtualenv.
For Python 2 use the following:

```
$ virtualenv .
$ bin/pip install -e '.[tests]'
$ bin/pip install pytest
$ bin/py.test src
```

For Python 3.4 use the following:

```
$ pythonn3.4 -m venv .
$ bin/pip install -e '.[tests]'
$ bin/pip install pytest
$ bin/py.test src
```

