#################
Development guide
#################

Here's how to set up `kafka-connect-manager` for local development.

1. Clone the `kafka-connect-manager <https://github.com/lsst-sqre/kafka-connect-manager>`_ repo from GitHub:

.. code-block:: bash

  $ git clone https://github.com/lsst-sqre/kafka-connect-manager.git

2. Install your local copy into a virtualenv:

.. code-block:: bash

  $ cd kafka-connect-manager
  $ virtualenv -p Python3 venv
  $ source venv/bin/activate
  $ make update

3. Create a branch for local development:

.. code-block:: bash

  $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

4. When you're done making changes, check that your changes pass the
lint checks, typing checks, and tests.

.. code-block:: bash

  $ tox -e lint typing py37

5. Commit your changes and push your branch to GitHub:

.. code-block:: bash

  $ git add .
  $ git commit -m "Your detailed description of your changes."
  $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for Python 3.
