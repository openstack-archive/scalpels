#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>
import os

from scalpels.db import api as db_api

def get_config(config):
    sc = {}
    # /opt/stack/data/ for devstack case
    # /opt/stack/
    data_dir = config.get("data_dir")

    # TODO replace these ugly codes
    actions = os.path.dirname(__file__)
    cli = os.path.dirname(actions)
    scalpels_py = os.path.dirname(cli)
    scalpels_package = os.path.dirname(scalpels_py)
    default_data_dir = os.path.join(scalpels_package, "scripts")
    sc["data_dir"] = data_dir if data_dir else default_data_dir
    return sc

def run(config):
    print "command setup: %s" % config
    sc = get_config(config)
    print "saving setup config: %s" % sc
    if config["force"]:
        db_api.db_drop()
        db_api.db_create(sc)
    else:
        db_api.db_create(sc)
