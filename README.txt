======================
silva.security.logging
======================

This extensions log in details user actions in Silva. To do so, you
need to add a *Silva Security Logging Service* in ZMI, in a site (either your
Silva Root or a local site).

You can configure the logging output. By default it will be logged in
the Zope logs.

You can log as well to a SQL database. In order to do this, you need
to configure a SQL connection in Zope to your database, and configure
your *Silva Security Logging Service* in ZMI to use it. The connection
should have a table called ``log`` created like this::

  create table log (
      username varchar(255),
      action varchar(255),
      time datetime,
      content varchar(512),
      content_intid bigint,
      info varchar(255))


The log storage is extensible, you can provide your own storage.
