#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.agents.server import server

def main():
    try:
        server.start()
        server.wait()
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    main()
