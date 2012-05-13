Development
===========

All assistance is appreciated! New features, documentation fixes, bug reports,
bug fixes, and more are graciously accepted.

Getting started
---------------

To get set up, fork the project on our `Github page`_. You can then
install from source by following the instructions in :doc:`install`. There are
a few additional dependencies for compiling the docs and running the tests:

* mock_
* unittest2_ (if on Python < 2.7)
* sphinx_ (for docs only)

You can install all dependencies using pip_ from the ``requirements.txt``
file:

.. code-block:: bash

    pip install -r requirements.txt

.. _Github page: https://github.com/jeffschenck/authorizesauce
.. _mock: http://www.voidspace.org.uk/python/mock/
.. _unittest2: http://pypi.python.org/pypi/unittest2
.. _sphinx: http://sphinx.pocoo.org/
.. _pip: http://www.pip-installer.org/

Running the tests
-----------------

Once you're all installed up, ensure that the tests pass by running them. You
can run the local unit tests with the following command:

.. code-block:: bash

    ./tests/run_tests.py

However, the above command skips some integration tests that actually hit the
remote Authorize.net test server. This is done so the main test suite can be
run quickly and without an internet connection. However, you should
occasionally run the full test suite, which can be done by setting an
environment variable:

.. code-block:: bash

    AUTHORIZE_LIVE_TESTS=1 ./tests/run_tests.py

Submitting bugs and patches
---------------------------

If you have a bug to report, please do so on our `Github issues`_ page. If
you've got a fork with a new feature or a bug fix with tests, please send us a
pull request.

.. _Github issues: https://github.com/jeffschenck/authorizesauce/issues
