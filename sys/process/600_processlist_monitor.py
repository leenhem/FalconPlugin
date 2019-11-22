#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Descripttion: 
@Author: leenhem
@Contact: leenhem.lh@gmail.com
@Date: 2019-10-29 18:27:27
@FilePath: /FalconPlugin/sys/process/60_processlist_monitor.py
'''

from subprocess import Popen, PIPE
import json
import time

data = []
endpoint="172.30.4.75"

def get_all_mountpoint():
    memory_data=[]
    cpu_data=[]
    p0=Popen(['ps','-aux'],stdout=PIPE,stderr=PIPE)
    raw_data = Popen(['sort','-k4nr'], stdin=p0.stdout, stdout=PIPE, stderr=PIPE)
    raw_data = Popen(['grep','-vE','%CPU|grep|-aux'], stdin=raw_data.stdout, stdout=PIPE, stderr=PIPE).communicate()[0]

    p0=Popen(['ps','-aux'],stdout=PIPE,stderr=PIPE)
    cpu=Popen(['sort','-k3nr'], stdin=p0.stdout, stdout=PIPE, stderr=PIPE)
    cpu = Popen(['grep','-vE','%CPU|grep|-aux'], stdin=cpu.stdout, stdout=PIPE, stderr=PIPE).communicate()[0]

    for i in raw_data.split('\n'):
        memory_data.append(i)
        if len(memory_data) == 10:break

    for i in cpu.split('\n'):
        cpu_data.append(i)
        if len(cpu_data) == 10:break
    return memory_data,cpu_data
    
if __name__ == "__main__":
    memory,cpu=get_all_mountpoint()
    for i in memory:
        process=i.split(' ')
        while '' in process:
            process.remove('')
        tmp_memory_percent={
                "endpoint":endpoint,
                "tags":"pid="+process[1]+",cmd="+' '.join(process[10:]),
                "timestamp":int(time.time()),
                "metric": "sys.process.memory.percent",
                "counterType":"GAUGE",
                "value":float(process[3]),
                "step": 600
                }
        data.append(tmp_memory_percent)
    for i in cpu:
        process=i.split(' ')
        while '' in process:
            process.remove('')
        tmp_cpu_percent={
                "endpoint":endpoint,
                "tags":"pid="+process[1]+",cmd="+' '.join(process[10:]),
                "timestamp":int(time.time()),
                "metric": "sys.process.cpu.percent",
                "counterType":"GAUGE",
                "value":float(process[2]),
                "step": 600
            }
        data.append(tmp_cpu_percent)
    print json.dumps(data)