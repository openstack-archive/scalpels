#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import argparse
from scalpels.cli.actions import load


def run(parser):
    config = parser.__dict__
    func = "run_%s" % config.pop("action")
    actioncall = getattr(load, func)
    ret = actioncall(config)

def main():
    rootparser = argparse.ArgumentParser(description="main entry point for scalpels")
    subparsers = rootparser.add_subparsers(title="actions", dest="action")

    # setup load actions
    load = subparsers.add_parser("load")
    load.add_argument("--storm", action="store_true", dest="storm", help="run concurrency nova boot")

    # setup start actions
    start = subparsers.add_parser("start")
    start.add_argument("--storm", action="store_true", dest="storm", help="run concurrency nova boot")

    # setup report actions
    report = subparsers.add_parser("report")

    # setup re-setup actions
    resetup = subparsers.add_parser("resetup")
    parser = rootparser.parse_args()
    try:
        run(parser)
    except Exception as e:
        print e
        return 1
    else:
        return 0

if __name__ == "__main__":
    main()
