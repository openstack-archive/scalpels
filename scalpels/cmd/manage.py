#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import os
import argparse
import psutil
import signal
from scalpels.db import api as db_api
from scalpels.client.api import api as agent_api

def get_default_tracer_dir():
    # /opt/stack/data/ for devstack case
    # /opt/stack/

    # TODO replace these ugly codes
    cmd = os.path.dirname(__file__)
    scalpels_py = os.path.dirname(cmd)
    scalpels_package = os.path.dirname(scalpels_py)
    default_data_dir = os.path.join(scalpels_package, "scripts")
    return default_data_dir

def do_setup(parser):
    data_opts = dict(parser.data_opts) if parser.data_opts else None
    tracer_opts = dict(parser.tracer_opts) if parser.tracer_opts else None
    if data_opts and data_opts.get("tracer_path") is None: # "" is meaningful sometime
        data_opts["tracer_path"] = get_default_tracer_dir()
    setup_config = {"data_opts":data_opts,
                    "force":parser.force,
                    "stat":parser.stat,
                    "tracer":tracer_opts}
    print "Setup config: %s" % setup_config
    if parser.force:
        print "recreating database"
        db_api.db_drop()
        db_api.db_create(setup_config)
    elif parser.data_opts is None and parser.tracer_opts is None and parser.stat is False:
        print "creating database"
        db_api.db_create(setup_config)

    if tracer_opts:
        print "registering tracer %s" % tracer_opts["name"]
        agent_api.register_tracer(tracer_opts)

    if parser.stat:
        raise NotImplementedError()

def do_stop(parser):
    # TODO call rpc server's stop API instead
    for p in psutil.process_iter():
        if p.as_dict()["cmdline"] and "sca-agent" in " ".join(p.cmdline):
            print "killing process %d, %s" % (p.pid, p.cmdline)
            p.send_signal(signal.SIGINT)
            return
    print "Can't find sca-agent process"
    return

def main():
    rootparser = argparse.ArgumentParser(description="main entry point for scalpels")
    subparsers = rootparser.add_subparsers(title="actions", dest="action")

    # setup re-setup actions
    setup = subparsers.add_parser("setup")
    setup.add_argument("-f", "--force", action="store_true", dest="force", help="re-create db")
    setup.add_argument("-d", "--data_opts", action="append", dest="data_opts", type=lambda kv:kv.split("="), help="data opts for tracer variables", required=False)
    setup.add_argument("-t", "--tracer_opts", action="append", dest="tracer_opts", type=lambda kv:kv.split("="), help="tracer opts for registering", required=False)
    setup.add_argument("-s", "--stat", action="store_true", dest="stat", help="setup stats for this agent")

    stop = subparsers.add_parser("stop")

    parser = rootparser.parse_args()

    if parser.action == "setup":
        do_setup(parser)

    if parser.action == "stop":
        do_stop(parser)

if __name__ == "__main__":
    main()
