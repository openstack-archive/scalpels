#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from oslo_config import cfg
import sys
from scalpels.db.sqlalchemy import BASE
from scalpels.db.sqlalchemy import models
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as oslodbsqa_utils
from copy import deepcopy as copy

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

def db_create(sc):
    BASE.metadata.create_all(get_engine())
    setup = models.Setup()
    setup.update({"config":sc})
    setup.save()
    return setup

def db_drop():
    BASE.metadata.drop_all(get_engine())

def model_query(model, session=None):
    if session is None:
        session = get_session()
    query = oslodbsqa_utils.model_query(model, session)
    return query

def result_create(name="", unit="", data=None, rtype=None):
    result = models.Result()
    result.update({"name":name,
                   "unit": unit,
                   "data":data,
                   "rtype": rtype if rtype else "unknown",
                  })
    result.save()
    return result

def task_create(results, pids):
    task = models.Task()
    task.update({"results":results, "pids":pids})
    task.save()
    return task

def task_update(task_uuid, results=None, pids=None):
    session = get_session()
    task = model_query(models.Task, session=session).filter_by(uuid=task_uuid).first()
    _update = dict()
    if results:
        _update["results"] = results
    if pids:
        _update["pids"] = pids
    task.update(_update)
    task.save(session=session)
    return task



def task_get(task_uuid, fuzzy=False):
    if not fuzzy:
        task = model_query(models.Task).filter_by(uuid=task_uuid).first()
        return task
    tasks = model_query(models.Task).all()
    matched = []
    for t in tasks:
        if t.uuid.startswith(task_uuid):
            matched.append(t)
    if len(matched) == 1:
        return matched[0]
    elif len(matched) > 1:
        raise ValueError("more than 1 result found by fuzzy search")
    elif len(matched) == 0:
        raise ValueError("not found result by fuzzy search")


def result_get(result_uuid):
    ret = model_query(models.Result).filter_by(uuid=result_uuid).first()
    return ret

def task_get_last():
    tasks = model_query(models.Task).all()
    if len(tasks) > 0:
        return tasks[-1]
    return None

def setup_config_get():
    setups = model_query(models.Setup).all()
    if len(setups) > 0:
        setup = setups[-1]
        return setup.config
    return None

def get_all_results():
    rets = model_query(models.Result).all()
    return rets

def register_tracer(name, template):
    tracer = models.Tracer()
    tracer.update({"name":name, "template": template})
    tracer.save()
    return tracer

def tracer_list():
    tracers = model_query(models.Tracer).all()
    return tracers

def update_config(data_opts):
    session = get_session()
    config = model_query(models.Setup, session=session).first()
    new = copy(config.config)
    new.update(data_opts)
    config.update({"config":new})
    config.save(session=session)
    return config

def get_config():
    config = model_query(models.Setup).first()
    return config.config
