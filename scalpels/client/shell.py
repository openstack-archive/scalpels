#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import argparse
import importlib


def run(parser):
    config = parser.__dict__
    modstr = "scalpels.client.actions.%s" % config.pop("action")
    mod = importlib.import_module(modstr)
    func = getattr(mod, "run")
    return func(config)


def main():
    rootparser = argparse.ArgumentParser(description="main entry of scalpels")
    subparsers = rootparser.add_subparsers(title="actions", dest="action")

    # setup load actions
    load = subparsers.add_parser("load")
    load.add_argument("--storm", action="store_true", dest="storm",
                      help="run concurrency nova boot")

    # setup start actions
    start = subparsers.add_parser("start")
    start.add_argument("-f", "--file", action="store", dest="file",
                       help="config file for this task", required=False)
    start.add_argument("-a", "--agent", action="append", dest="agent",
                       help="agent(s) to run", required=False)

    # setup stop actions
    stop = subparsers.add_parser("stop")
    stop.add_argument("--last", action="store_true", dest="last",
                      help="report the last task")
    stop.add_argument("uuid", type=str, default="", nargs="?",
                      help="report the last task")
    stop.add_argument("-a", "--agent", action="append", dest="agent",
                      help="agent(s) to stop", required=False)

    # setup report actions
    report = subparsers.add_parser("report")
    report.add_argument("--last", action="store_true", dest="last",
                        help="report the last task")
    report.add_argument("--html", action="store_true", dest="html",
                        help="report html to stdout instead of pretty print")
    report.add_argument("uuid", type=str, default="", nargs="?",
                        help="report the last task")
    report.add_argument("-a", "--agent", action="append", dest="agent",
                        help="agent(s) to stop", required=False)

    # setup sca result --list
    result = subparsers.add_parser("result")
    result.add_argument("-l", "--list", action="store_true", dest="list",
                        help="list all results from db")
    result.add_argument("uuid", type=str, default="", nargs="?",
                        help="report the last task")
    result.add_argument("--html", action="store_true", dest="html",
                        help="report html to stdout instead of pretty print")
    result.add_argument("--short", action="store_true", dest="short",
                        help="report uuid only")

    # agent command
    tracer = subparsers.add_parser("tracer")
    tracer.add_argument("-l", "--list", action="store_true", dest="list",
                        help="list all agents")

    parser = rootparser.parse_args()
    try:
        run(parser)
    except Exception as e:
        raise e
    else:
        return 0

if __name__ == "__main__":
    main()
