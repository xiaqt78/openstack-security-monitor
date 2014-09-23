import os
import time
import multiprocessing
import signal
import commands
import socket
import sys

'''
   This scripts is used to collect data of a mirrored port in IIIS data center of System Group,
   and one file will be generated every hour which name is composed of string 'Sniff_f_' ,date and time.
   2014-05-24  create
   2014-07-01  modify to c/s mode,this scripts run as server
   developed by Xia Qingtang,IIIS System Group
'''


#terminate the process of tcpdump when timeout
def TerminateProsPid():
    cmd='ps aux | grep tcpdump'
    
    info=commands.getoutput(cmd)      #info which save the consequence of 'ps aux | grep tcpdump'
    infos=info.split('\n')            #split the consequence by line
    linfos=len(infos)
 
    i=0
    while i<linfos:                 #two process represent 'ps aux|grep tcpdump'and itself
        infoss=infos[i].split()       #split one line by spaces

        if infoss[10]=='tcpdump':
            os.kill(int(infoss[1]), signal.SIGTERM)      #kill a timeout process
            
        i+=1


#class of tcpdump process
class Tcpdumpprocess(multiprocessing.Process):
    def __init__(self,file_name,eth_card):
        multiprocessing.Process.__init__(self)
        self.file_name=file_name
        self.eth_card=eth_card
        
    def run(self):
        os.system('tcpdump -i '+self.eth_card+' -w '+'/home/xqt/projectshare/mirrorfiles/'+self.file_name)
        
    def __del__(self):
        TerminateProsPid()
        

#main function,collecting data to a file
if __name__=='__main__':

    fhead='Sniff_f_'

    TerminateProsPid()     #At first,terminate any tcpdump process. Two reason:1 perhaps this program is terminate in exception 2 other run tcpdump on the interface

    #receive command from client, command format: file suffix + mirror time + eth_card
    port=8089
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind(("" ,port))
    print 'waiting on port:',port
    #loop handling
    while True:
        data,addr=s.recvfrom(1024)
        #if no data,no need to handle
        if len(data)>0:
            #interprete message
            list_data=data.split()
            eth_card=list_data[2]

            Now_Date_Time=time.localtime()  #use date and time to save the sniffering data
            file_name=fhead+str(Now_Date_Time.tm_year)+str(Now_Date_Time.tm_mon)+str(Now_Date_Time.tm_mday)+str(Now_Date_Time.tm_hour)+str(Now_Date_Time.tm_min)+str(Now_Date_Time.tm_sec)+list_data[0]+'.cap'

            print "Received mirror command message from ",addr,"\r\n File name:\r\n",file_name
            p=Tcpdumpprocess(file_name,eth_card)

            p.start()                     #start a process

            time.sleep(int(list_data[1]))              #restart a tcpdump process to sniffer,and generate a file again  (if modify to multiprocess, this should be move to run())

            TerminateProsPid()            #terminate previous tcpdump process (if modify to multiprocess, this should be move to run(), obtain pid to terminate)

    '''
    while True:
        Now_Date_Time=time.localtime()  #use date and time to save the sniffering data
        
        file_name=fhead+str(Now_Date_Time.tm_year)+str(Now_Date_Time.tm_mon)+str(Now_Date_Time.tm_mday)+str(Now_Date_Time.tm_hour)+str(Now_Date_Time.tm_min)+str(Now_Date_Time.tm_sec)+'.cap'
        p=Tcpdumpprocess(file_name,eth_card) 
        p.start()                     #start a process
        
        time.sleep(30)              #restart a tcpdump process to sniffer,and generate a file again
        
        TerminateProsPid()            #terminate previous tcpdump process
    '''

        

