#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

import json
import subprocess

from kombu import Connection
from kombu import Exchange
from kombu.mixins import ConsumerMixin
from kombu import Queue

task_exchange = Exchange('amq.rabbitmq.trace', type='topic')
task_queues = []

debug ={"method": set(),
        "result": set()}

grep = "method:object_action.objinst"
grep = "method:object_action.Compute"
grep = "result"
grep = "result.nova_object"

if "." not in grep:
    grep = grep + "."
head, hint = grep.split(".", 1)

print_method = print_result = False

if head.startswith("method:"):
    print_method = True
elif head == "result":
    print_result = True

print_method = True
print_result = True

class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=task_queues,
                accept=['pickle', 'json'],
                callbacks=[self.process_task])]

    # TODO get req if hint in resp
    def process_task(self, body, message):
        oslo_body = json.loads(json.loads(body)['oslo.message'])
        if print_method and "method" in oslo_body:
            method = head.split(":", 1)[1]
            if hint in str(oslo_body) and method == oslo_body["method"]:
                print "[method:%s] %s\n" % (method, oslo_body)
        elif print_result and "result" in oslo_body:
            if hint in str(oslo_body):
                print "[result] %s\n" % oslo_body

with Connection('amqp://guest:guest@localhost:5672//') as conn:
    chan = conn.channel()
    queue = Queue("trace_", task_exchange, routing_key="publish.*", channel=chan)
    task_queues.append(queue)
    try:
        subprocess.check_call("sudo rabbitmqctl trace_on", shell=True)
        worker = Worker(conn)
        worker.run()
    except KeyboardInterrupt:
        subprocess.check_call("sudo rabbitmqctl trace_off", shell=True)
        queue.delete()
