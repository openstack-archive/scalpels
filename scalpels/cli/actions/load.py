#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>


def run(config):
    loads = (k for k in config if config[k])
    for load in loads:
        func = "load_%s" % load
        try:
            loadcall = globals()[func]
        except KeyError:
            continue
        loadcall(config)

def load_storm(config):
    #TODO use novaclient python api to do this
    print "now, let's run nova boot api in current."
