#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import argparse
import os
import signal

import psutil

from scalpels.client import api
from scalpels.db import api as db_api


agent_api = api.api


def get_default_tracer_dir():
    # /opt/stack/data/ for devstack case
    # /opt/stack/

    # TODO(kun) replace these ugly codes
    cmd = os.path.dirname(__file__)
    scalpels_py = os.path.dirname(cmd)
    scalpels_package = os.path.dirname(scalpels_py)
    default_data_dir = os.path.join(scalpels_package, "scripts")
    return default_data_dir


def do_db(parser):
    setup_config = {"tracer_path": get_default_tracer_dir()}
    if parser.force:
        print "recreating database"
        db_api.db_drop()
        db_api.db_create(setup_config)
    else:
        print "creating database"
        db_api.db_create(setup_config)


def do_setup(parser):
    data_opts = dict(parser.data_opts) if parser.data_opts else None

    if data_opts:
        agent_api.update_config(data_opts)

    tracer_opts = dict(parser.tracer_opts) if parser.tracer_opts else None

    if tracer_opts:
        print "registering tracer %s" % tracer_opts["name"]
        agent_api.register_tracer(tracer_opts)

    if parser.stat:
        config = agent_api.get_config()
        import prettytable
        t = prettytable.PrettyTable(["key", "value"])
        for k, v in config.items():
            t.add_row([k, v])
        print t


def do_stop(parser):
    # TODO(kun) call rpc server's stop API instead
    for p in psutil.process_iter():
        if p.as_dict()["cmdline"] and "sca-agent" in " ".join(p.cmdline):
            print "killing process %d, %s" % (p.pid, p.cmdline)
            p.send_signal(signal.SIGINT)
            return
    print "Can't find sca-agent process"
    return


def main():
    rootparser = argparse.ArgumentParser(description="entry point of scalpels")
    subparsers = rootparser.add_subparsers(title="actions", dest="action")

    # db actions
    db = subparsers.add_parser("db-create")
    db.add_argument("-f", "--force", action="store_true",
                    dest="force", help="re-create db")

    # setup re-setup actions
    setup = subparsers.add_parser("setup")
    setup.add_argument("-d", "--data_opts", action="append", dest="data_opts",
                       type=lambda kv: kv.split("="),
                       help="data opts for tracer variables", required=False)
    setup.add_argument("-t", "--tracer_opts", action="append",
                       dest="tracer_opts", type=lambda kv: kv.split("="),
                       help="tracer opts for registering", required=False)
    setup.add_argument("-s", "--stat", action="store_true", dest="stat",
                       help="setup stats for this agent")

    stop = subparsers.add_parser("stop")  # noqa

    parser = rootparser.parse_args()

    if parser.action == "db-create":
        do_db(parser)

    if parser.action == "setup":
        do_setup(parser)

    if parser.action == "stop":
        do_stop(parser)


if __name__ == "__main__":
    main()
