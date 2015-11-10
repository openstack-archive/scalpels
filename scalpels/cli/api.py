#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>


from scalpels.cli.rpcapi import rpcapi

class API(object):
    def __init__(self):
        pass

    def get_tracer_list(self):
        return rpcapi.tracer_list()

    def start_tracers(self, tracers):
        rpcapi.start_tracers(tracers=tracers)

    def stop_task(self, config):
        rpcapi.stop_task(config)

api = API()
