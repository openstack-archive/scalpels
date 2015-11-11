#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.agents.server import server

def main():
    # TODO handle stop later
    server.start()
    server.wait()

if __name__ == "__main__":
    main()
