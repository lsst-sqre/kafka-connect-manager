##########
Change log
##########

0.8.0 (2020-08-05)
------------------
* Use data classes for the application and connector configuration.
* Plugin like organization, to support new connectors add a cli and a config file.
* Add support to the Amazon S3 Sink connector

0.7.2 (2020-03-31)
------------------
* Add support to the InfluxDB Sink Connector.
* Add --timestamp option to select the timestamp field to use in the InfluxDB Sink connector.
* Fix Header Converter Class configuration setting.
* Fix ``tasks.max`` configuration setting name.
* Add connector ``name`` configuration setting to support multiple connectors of the same class.
* Handle empty list of topics properly.
