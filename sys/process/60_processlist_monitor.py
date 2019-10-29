#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE
import json
import time

data = []
endpoint="172.30.4.75"

def get_all_mountpoint():
    data=[]
    p0=Popen(['ps','-aux'],stdout=PIPE,stderr=PIPE)
    raw_data = Popen(['sort','-k4nr'], stdin=p0.stdout, stdout=PIPE, stderr=PIPE).communicate()[0]
    for i in raw_data.split('\n'):
        data.append(i)
        if len(data) == 60:break
    return data
    
if __name__ == "__main__":
    list=get_all_mountpoint()
    for i in list:
        process=i.split(' ')
        while '' in process:
            process.remove('')
        tmp_memory_percent={
                "endpoint":endpoint,
                "tags":"pid="+process[1]+",cmd="+' '.join(process[10:]),
                "timestamp":int(time.time()),
                "metric": "sys.process.memory.percent",
                "counterType":"GAUGE",
                "value":process[3],
                "step": 60
                }

        tmp_cpu_percent={
                "endpoint":endpoint,
                "tags":"pid="+process[1]+",cmd="+' '.join(process[10:]),
                "timestamp":int(time.time()),
                "metric": "sys.process.cpu.percent",
                "counterType":"GAUGE",
                "value":process[4],
                "step": 60
            }
        data.append(tmp_cpu_percent)
        data.append(tmp_memory_percent)
    print json.dumps(data)