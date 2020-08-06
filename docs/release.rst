
=================
Release procedure
=================

A reminder for the maintainers on how to make a new release. Releases are made
by creating a Git tag with a semantic version and pushing to GitHub.

Make sure all your changes are committed (including an entry in CHANGELOG.rst).
Then run:

.. code-block:: bash

  $ git tag -s X.Y.Z -m "X.Y.Z"
  $ git push
  $ git push --tags

A GitHub action will build the new version and upload to Docker Hub.
