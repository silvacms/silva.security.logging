======================
silva.security.logging
======================


Logging into a SQL database. You need to create a table::

  create table log (
      username varchar(255),
      action varchar(255),
      time datetime,
      content varchar(512),
      content_intid bigint,
      info varchar(255))


