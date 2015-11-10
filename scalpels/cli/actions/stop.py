#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.db import api as db_api
import psutil
import signal
from scalpels.cli.api import api as agent_api

LOWEST=8

def get_last_task():
    last_task = db_api.task_get_last()
    return last_task

def run(config):
    agent_api.stop_task(config)
