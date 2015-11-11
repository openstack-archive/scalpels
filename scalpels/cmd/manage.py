#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from scalpels.agents.server import server

def main():
    server.start()
    server.wait()

if __name__ == "__main__":
    main()
