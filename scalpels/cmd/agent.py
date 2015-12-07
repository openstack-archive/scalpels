#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from oslo_config import cfg
from oslo_log import log as logging

from scalpels.agents import server


def main():
    # TODO(kun) handle stop later
    logging.register_options(cfg.CONF)
    logging.setup(cfg.CONF, "scalpels")
    server.server.start()
    server.server.wait()


if __name__ == "__main__":
    main()
