#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.agents.server import server
from oslo_log import log as logging
from oslo_config import cfg

def main():
    # TODO handle stop later
    logging.register_options(cfg.CONF)
    logging.setup(cfg.CONF, "scalpels")
    server.start()
    server.wait()

if __name__ == "__main__":
    main()
