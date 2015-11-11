#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import os
import argparse
from scalpels.db import api as db_api

def get_setup_config(parser):
    sc = {}
    # /opt/stack/data/ for devstack case
    # /opt/stack/
    data_dir = parser.data_dir

    # TODO replace these ugly codes
    cmd = os.path.dirname(__file__)
    scalpels_py = os.path.dirname(cmd)
    scalpels_package = os.path.dirname(scalpels_py)
    default_data_dir = os.path.join(scalpels_package, "scripts")
    sc["data_dir"] = data_dir if data_dir else default_data_dir
    return sc

def do_setup(parser):
    sc = get_setup_config(parser)
    print "Setup config: %s" % sc
    if parser.force:
        db_api.db_drop()
        db_api.db_create(sc)
    else:
        db_api.db_create(sc)

def main():
    rootparser = argparse.ArgumentParser(description="main entry point for scalpels")
    subparsers = rootparser.add_subparsers(title="actions", dest="action")

    # setup re-setup actions
    setup = subparsers.add_parser("setup")
    setup.add_argument("-f", "--force", action="store_true", dest="force", help="re-create db")
    setup.add_argument("-d", "--data_dir", action="store", dest="data_dir",  help="data dir where to find script resources", required=False)

    parser = rootparser.parse_args()

    if parser.action == "setup":
        do_setup(parser)

if __name__ == "__main__":
    main()
