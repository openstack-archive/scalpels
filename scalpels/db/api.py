#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>


from oslo_db import api as db_api
from oslo_db import options as db_options
from oslo_config import cfg
CONF = cfg.CONF


IMPL = db_api.DBAPI("sqlalchemy", backend_mapping={"sqlalchemy":"scalpels.db.sqlalchemy.api"})

db_options.set_defaults(CONF, connection="sqlite:////tmp/scalpels.sqlite", sqlite_db="scalpels.sqlite")

def db_create(sc):
    IMPL.db_create(sc)

def db_drop():
    IMPL.db_drop()

def result_create(data):
    """
    :param data: a list :)
    :returns: result model obj
    """
    return IMPL.result_create(data)

def task_create(results, pids):
    """
    :param results: a list contains result.uuid
    :returns: task model obj
    """
    return IMPL.task_create(results, pids)

def task_get(task_uuid, fuzzy=False):
    return IMPL.task_get(task_uuid, fuzzy)

def task_update(task_uuid, results=None, pids=None):
    return IMPL.task_update(task_uuid, results, pids)

def task_get_last():
    return IMPL.task_get_last()

def result_get(result_uuid):
    """
    :returns : dict, with data and its metadata
    """
    return IMPL.result_get(result_uuid)

def setup_config_get():
    """
    :returns : dict
    """
    return IMPL.setup_config_get()
