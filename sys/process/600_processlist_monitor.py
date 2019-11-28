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
    p0=Popen(['ps','-eo','user,pid,pcpu,pmem,lstart,etime,command'],stdout=PIPE,stderr=PIPE).communicate()[0]
    processList=[]
    for i in p0.split('\n'):
        list=[]        
        for j in i.split(' '):
            if j != '':list.append(j)
        cmd=' '.join(list[10:])[:50]
        del list[10:len(list)]
        list.append(cmd)
        if len(list) == 11: 
            list[2]=float(list[2]) #CPU转数值型
            list[3]=float(list[3]) #Memory转数值型
            if list[2] >0 or list[3] >0:
                import time
                dateTime=list[4]+' '+list[5]+' '+list[6]+' '+list[7]+' '+list[8]
                processTime=time.mktime(time.strptime(dateTime,'%a %b %d %H:%M:%S %Y')) #Mon Sep 23 17:21:11 2019 转换为时间戳
                nowTime=time.time()
                del list[4:9]
                list.insert(4,processTime) #把日期改为时间戳
                if nowTime-processTime > 600:
                    processList.append(list) # cpu内存<=0的不取
    return processList

if __name__ == "__main__":
    processList=get_all_mountpoint()
    for process in sorted(processList,key=lambda x:x[3],reverse=True)[:5]: #取Memory前5
        if process[3]<=0:break
        tmp_memory_percent={
                "endpoint":endpoint,
                "tags":"pid="+process[1]+",cmd="+process[6],
                "timestamp":int(time.time()),
                "metric": "sys.process.memory.percent",
                "counterType":"GAUGE",
                "value":process[3],
                "step": 600
                }
        data.append(tmp_memory_percent)
    for process in sorted(processList,key=lambda x:x[2],reverse=True)[:5]: #取CPU前5
        if process[2]<=0:break
        tmp_cpu_percent={
                "endpoint":endpoint,
                "tags":"pid="+process[1]+",cmd="+process[6],
                "timestamp":int(time.time()),
                "metric": "sys.process.cpu.percent",
                "counterType":"GAUGE",
                "value":process[2],
                "step": 600
            }
        data.append(tmp_cpu_percent)
    print json.dumps(data)