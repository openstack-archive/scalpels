#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

from novaclient import client
import os

def run(config):
    loads = (k for k in config if config[k])
    for load in loads:
        func = "load_%s" % load
        try:
            loadcall = globals()[func]
        except KeyError:
            continue
        loadcall(config)

def get_creds_from_env():
    user = os.environ.get("OS_USERNAME")
    pw = os.environ.get("OS_PASSWORD")
    tenant = os.environ.get("OS_TENANT_NAME")
    auth_url= os.environ.get("OS_AUTH_URL")
    return (user, pw, tenant, auth_url)

def nova_boot_bulk():
    creds = get_creds_from_env()
    if None in creds:
        raise ValueError("can't find all necessary creds from env: %s" % creds)
    nova = client.Client(2, *creds)
    image = nova.images.get("a1e6a7a5-2e77-42a6-8417-1f47ba7ba911")
    flavor = nova.flavors.get("3")
    nics = [{"net-id":"c5e2d25d-72ef-4ef4-b39e-f10027f9289d"}]
    ret = nova.servers.create(name="bulk-foo", image=image, flavor=flavor, min_count=2, max_count=2, nics=nics)
    print "we got %s" % ret
    return

def load_storm(config):
    #TODO use novaclient python api to do this
    nova_boot_bulk()
