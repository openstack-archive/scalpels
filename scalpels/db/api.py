#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>


from oslo_db import api as db_api
from oslo_db import options as db_options
from oslo_config import cfg
CONF = cfg.CONF


IMPL = db_api.DBAPI("sqlalchemy", backend_mapping={"sqlalchemy":"scalpels.db.sqlalchemy.api"})

db_options.set_defaults(CONF, connection="sqlite:////tmp/scalpels.sqlite", sqlite_db="scalpels.sqlite")

def db_create():
    IMPL.db_create()

def db_drop():
    IMPL.db_drop()

def result_create(data):
    """
    :param data: a list :)
    :returns: result model obj
    """
    return IMPL.result_create(data)

def task_create(results):
    """
    :param results: a list contains result.uuid
    :returns: task model obj
    """
    return IMPL.task_create(results)

def task_get(task_uuid):
    return IMPL.task_get(task_uuid)

def task_get_last():
    return IMPL.task_get_last()

def result_get(result_uuid):
    """
    :returns : dict, with data and its metadata
    """
    return IMPL.result_get(result_uuid)
