import os,time,sys,subprocess
from config import *
cwd=os.getcwd()
if MULTI_PROCESSING == False:
    subprocess.run(PYTHON+' '+cwd+'\\main.py')
elif MULTI_PROCESSING == True:
    for i in range(1,THREAD+2):
        os.system('start '+PYTHON+' '+cwd+'\\main.py '+str(i))
else:
    print('错误：不存在的集群选项。请检查 config.py 并修改 MULTI_PROCESSING 设置，然后重新启动DSN环境。')
exit(0)