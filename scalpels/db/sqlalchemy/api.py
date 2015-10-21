#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from oslo_config import cfg
import sys
from scalpels.db.sqlalchemy import BASE
from scalpels.db.sqlalchemy import models
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as oslodbsqa_utils

CONF = cfg.CONF

_FACADE = None

def _create_facade_lazily():
    global _FACADE

    if _FACADE is None:
        _FACADE = db_session.EngineFacade.from_config(CONF)

    return _FACADE

def get_engine():
    facade = _create_facade_lazily()
    return facade.get_engine()

def get_session(**kwargs):
    facade = _create_facade_lazily()
    return facade.get_session(**kwargs)

def get_backend():
    return sys.modules[__name__]

def db_create():
    BASE.metadata.create_all(get_engine())

def db_drop():
    BASE.metadata.drop_all(get_engine())

def model_query(model, session=None):
    if session is None:
        session = get_session()
    query = oslodbsqa_utils.model_query(model, session)
    return query

def result_create(data):
    result = models.Result()
    result.update({"data":data})
    result.save()
    return result

def task_create(results):
    task = models.Task()
    task.update({"results":results})
    task.save()
    return task

def task_get(task_uuid):
    task = model_query(models.Task).filter_by(uuid=task_uuid).first()
    return task


def result_get(result_uuid):
    ret = model_query(models.Result).filter_by(uuid=result_uuid).first()
    return ret

def task_get_last():
    tasks = model_query(models.Task)
    return tasks[-1]
