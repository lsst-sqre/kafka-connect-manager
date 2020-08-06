.. _configuration:

######################
Configuration settings
######################

In this section we present the main configuration settings for each of the supported connectors.

The configuration classes are also documented here and can be used as reference for the configuration settings exposed in the `values.yaml`_ when using the :ref:`helm-chart`.

.. _values.yaml: https://github.com/lsst-sqre/charts/blob/master/charts/kafka-connect-manager/values.yaml


.. automodapi:: kafkaconnect.config

.. automodapi:: kafkaconnect.influxdb_sink.config

.. automodapi:: kafkaconnect.s3_sink.config
