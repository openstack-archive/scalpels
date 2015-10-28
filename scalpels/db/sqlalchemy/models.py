#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import uuid
import json

from sqlalchemy import types as sqa_types
from scalpels.db.sqlalchemy import BASE
from sqlalchemy import (Column, Integer, String)
from oslo_db.sqlalchemy import models as oslodbmodels


class JSONEncodedData(sqa_types.TypeDecorator):
    impl = sqa_types.Text
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class ScalpelsBase(oslodbmodels.ModelBase, oslodbmodels.TimestampMixin):
    def save(self, session=None):
        if session is None:
            from scalpels.db.sqlalchemy import api
            session = api.get_session()

        super(ScalpelsBase, self).save(session=session)

class Task(BASE, ScalpelsBase):
    __tablename__ =  "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), default=lambda : str(uuid.uuid4()), nullable=False)
    results = Column(JSONEncodedData, nullable=False)
    pids = Column(JSONEncodedData, nullable=False)

class Result(BASE, ScalpelsBase):
    __tablename__ =  "result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), default=lambda : str(uuid.uuid4()), nullable=False)
    data = Column(JSONEncodedData, nullable=False)
    unit = Column(String(20), nullable=True)

class Setup(BASE, ScalpelsBase):
    __tablename__ = "setup"
    id = Column(Integer, primary_key=True, autoincrement=True)
    config = Column(JSONEncodedData, nullable=False)
