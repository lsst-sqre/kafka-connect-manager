.. _installation:

##################
Installation guide
##################

kafka-connect-manager is meant to be run on Kubernetes and it assumes that Kafka is running in the same kubernetes cluster.

This section shows how to use the `Helm chart`_ to install kafka-connect-manager.
The main configuration settings you need to know for each of the supported connector are covered in the :ref:`configuration` section.


.. _`helm-chart`: https://lsst-sqre.github.io/charts

Helm chart
==========

There is a Helm chart for kafka-connect-manager available from the `Rubin Observatory charts repository`_. To use the Helm chart, set the appropriate configuration values in the `values.yaml`_ file.

.. _Rubin Observatory charts repository: https://lsst-sqre.github.io/charts
.. _values.yaml: https://github.com/lsst-sqre/charts/blob/master/charts/kafka-connect-manager/values.yaml


Argo CD
=======

kafka-connect-manager is deployed using Argo CD. An example of Argo CD app using the Helm chart can be found `here <https://github.com/lsst-sqre/argocd-efd/tree/master/apps/s3-sink>`_.
