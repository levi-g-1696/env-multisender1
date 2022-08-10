import json,time
import datetime
import subprocess
import sys,os


if len(sys.argv) < 2:
    print ("You must set argument!!!")

else:
    os.chdir("..")
    print ("going root")

    with open('initConfig.json') as f:
      d = json.load(f)
      map= d["mailAlertPeriod"]
      print("d.mailAlertPeriod", map)

current_time = "t="+ time.strftime( " %D %H:%M:%S", time.localtime())
print(current_time)
with open("C:\\Users\\wn10\\PycharmProjects\\multisender1.0\\Alert.txt", 'r') as f:
    lines = f.read().splitlines()
    last_line = lines[-2]

#line = subprocess.check_output(['tail', '-1', "C:\\Users\\wn10\\PycharmProjects\\multisender1.0\\Alert.txt"])
print(last_line)
folder1=r"C:\Users\wn10\PycharmProjects\multisender1.0\output"
folder2= r"C:\Users\wn10\Downloads\HMH4_20211123_1805"
t1m=os.path.getmtime(folder1)
t2m=os.path.getmtime(folder2)
t1c=os.path.getctime(folder1)

t2c=os.path.getctime(folder2)
tnow = time.time()
print( "t1c                  t1m")
print (t1c, t1m)
print (t2c, t2m)
print (tnow)