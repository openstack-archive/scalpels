#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import argparse
import importlib


def run(parser):
    config = parser.__dict__
    modstr = "scalpels.cli.actions.%s" % config.pop("action")
    mod = importlib.import_module(modstr)
    func = getattr(mod, "run")
    return func(config)

def main():
    rootparser = argparse.ArgumentParser(description="main entry point for scalpels")
    subparsers = rootparser.add_subparsers(title="actions", dest="action")

    # setup load actions
    load = subparsers.add_parser("load")
    load.add_argument("--storm", action="store_true", dest="storm", help="run concurrency nova boot")

    # setup start actions
    start = subparsers.add_parser("start")
    start.add_argument("-f", "--file", action="store", dest="file", help="config file for this task", required=False)
    start.add_argument("-a", "--agent", action="append", dest="agent", help="agent(s) to run", required=False)

    # setup stop actions
    stop = subparsers.add_parser("stop")
    stop.add_argument("--last", action="store_true", dest="last", help="report the last task")
    stop.add_argument("uuid", type=str, default="", nargs="?", help="report the last task")

    # setup report actions
    report = subparsers.add_parser("report")
    report.add_argument("--last", action="store_true", dest="last", help="report the last task")
    report.add_argument("uuid", type=str, default="", nargs="?", help="report the last task")

    # setup re-setup actions
    setup = subparsers.add_parser("setup")
    setup.add_argument("-f", "--force", action="store_true", dest="force", help="re-create db")
    setup.add_argument("-d", "--data_dir", action="store", dest="data_dir",  help="data dir where to find script resources", required=False)

    parser = rootparser.parse_args()
    try:
        run(parser)
    except Exception as e:
        raise
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()
