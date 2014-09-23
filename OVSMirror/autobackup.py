__author__ = 'root'
import os
import time
i=1
while True:
    os.system('scp ./*.* xqt@10.1.0.152:/home/xqt/importantbackup/soft-develop-by-xqt')
    print 'scp times:'+str(i)
    i=i+1
    time.sleep(2)

