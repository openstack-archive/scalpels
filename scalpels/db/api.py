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

def result_create(name="", unit="", data=None, rtype=None):
    """
    :param data: a list :)
    :returns: result model obj
    """
    return IMPL.result_create(name, unit, data, rtype)

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

def task_append_result(task_uuid, result_uuid):
    return IMPL.task_append_result(task_uuid, result_uuid)

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

def get_all_results():
    return IMPL.get_all_results()

def register_tracer(name, template):
    return IMPL.register_tracer(name, template)

def tracer_list():
    return IMPL.tracer_list()

def update_config(data_opts):
    return IMPL.update_config(data_opts)

def get_config():
    return IMPL.get_config()

def tracer_get(tracer):
    """
    param tracer: tracer name, like, 'rpc'
    """
    return IMPL.tracer_get(tracer)

def tracer_update(tracer, running=None, pid=None):
    return IMPL.tracer_update(tracer, running, pid)

def tracer_append_result(tracer, result_uuid):
    return IMPL.tracer_append_result(tracer, result_uuid)
