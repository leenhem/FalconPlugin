#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil
import time,json
endpoint="172.30.4.75"
class process():
    def getProcessCpu(self,res):
        result=[]
        for i in res:
            p = psutil.Process(i["pid"])
            tmp_memory_percent={
                "endpoint":endpoint,
                "tags":"pid="+str(i["pid"])+",name="+i["name"]+",cmd="+'\t'.join(p.cmdline()),
                "timestamp":int(time.time()),
                "metric": "sys.process.memory.percent",
                "counterType":"GAUGE",
                "value":p.memory_percent(),
                "step": 90
                }
            tmp_cpu_percent={
                "endpoint":endpoint,
                "tags":"pid="+str(i["pid"])+",name="+i["name"]+",cmd="+'\t'.join(p.cmdline()),
                "timestamp":int(time.time()),
                "metric": "sys.process.cpu.percent",
                "counterType":"GAUGE",
                "value":p.cpu_percent(interval=1),
                "step": 90
            }
            result.append(tmp_memory_percent)
            result.append(tmp_cpu_percent)
        return result
if __name__ == "__main__":
    result=[]
    m=process()
    for i in psutil.process_iter():
        ps = i.as_dict(attrs=["pid","name"])
        p = psutil.Process(ps["pid"])
        ps["memory"]=p.memory_percent()
        result.append(ps)
    result=sorted(result,key=lambda x: x["memory"],reverse=True)[0:60]
    res=m.getProcessCpu(result)
    print json.dumps(res)