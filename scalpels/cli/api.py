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

    def stop_task(self, uuid):
        rpcapi.stop_task(uuid=uuid)

    def get_task(self, uuid, fuzzy=False):
        return rpcapi.get_task(uuid=uuid, fuzzy=fuzzy)

    def get_latest_task(self):
        return rpcapi.get_latest_task()

    def get_result(self, uuid):
        return rpcapi.get_result(uuid=uuid)

    def get_all_results(self):
        return rpcapi.get_all_results()

api = API()
