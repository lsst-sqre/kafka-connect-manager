.. _installation:

##################
Installation guide
##################

kafkaconnect is meant to be run on Kubernetes and it assumes that Kafka is running in the same kubernetes cluster.

This section shows how to use the kafka-connect-manager `Helm chart`_.


Helm chart
==========

The kafka-connect-manager `Helm chart`_ creates a configmap with the configuration used by kafkaconnect to create the connector.
Secrets are obtained from a Kubernetes secret configured in the values.yaml file, and then injected in the environment.
Kafkaconnect uses the environment variables to inject the secrets in the connector configuration before uploading it.

.. _Helm chart: https://github.com/lsst-sqre/charts/blob/master/charts/kafka-connect-manager


Argo CD
=======

An example of Argo CD app using the Helm chart can be found `here`_.

.. _here: https://github.com/lsst-sqre/argocd-efd/tree/master/apps/kafka-connect-manager