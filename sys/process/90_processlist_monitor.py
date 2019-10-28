#coding:utf-8
import psutil
import time,json
endpoint="10.17.116.3"
class process():
    def getProcessCpu(self,res):
        result=[]
        for i in res:
            p = psutil.Process(i["pid"])
            tmp_memory_percent={
                "Endpoint":endpoint,
                "TAGS":"",
                "Timestamp":int(time.time()),
                "Metric": "sys.process.memory.percent",
                "CounterType":"GAUGE",
                "pid":i["pid"],
                "Value":p.memory_percent(),
                "name":i["name"],
                "cmd": ' '.join(p.cmdline()),
                "Step": 90
                }
            tmp_cpu_percent={
                "Endpoint":endpoint,
                "TAGS":"",
                "Timestamp":int(time.time()),
                "Metric": "sys.process.cpu.percent",
                "CounterType":"GAUGE",
                "pid":i["pid"],
                "Value":p.cpu_percent(interval=1),
                "name":i["name"],
                "cmd": ' '.join(p.cmdline()),
                "Step": 90
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