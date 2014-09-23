__author__ = 'root'
import sys
import pxssh
import pxssh1
import time
import socket
import multiprocessing
import math
import os

'''
   This scripts is used to collect data of a mirrored port in IIIS data center of System Group,
   This scripts will set the switch to be mirroring and send command message to a host attached to it.
   When finished the collecting data process, this scripts will delete the mirror settings on the switch.
   2014-06-29  create
   2014-07-01  modify to c/s mode,this scripts run as client
   2014-07-03  completed
   developed by Xia Qingtang,IIIS System Group
'''

#login the mirrored switches through username and pwd
username=''
pwd=''

#switch ,host , switch-port , host-eth-card relation
#PS1-24  AS1-24
dict_switch_host={'10.0.3.1':['10.1.0.12','12','eth0'],'10.0.3.2':['10.1.0.16','1','eth0'],'10.0.3.3':['10.1.0.31','1','eth0'],'10.0.3.4':['10.1.0.46','1','eth0'],'10.0.3.5':['10.1.0.61','1','eth0'],
                  '10.0.3.6':['10.1.0.76','1','eth0'],'10.0.3.7':['10.1.0.91','1','eth0'],'10.0.3.8':['10.1.0.106','1','eth0'],'10.0.3.9':['10.1.0.121','1','eth0'],'10.0.3.10':['10.1.0.136','1','eth0'],
                  '10.0.3.11':['10.1.0.151','1','eth0'],'10.0.3.12':['10.1.0.166','1','eth0'],
                  '10.0.3.13':['10.1.0.14','14','eth2'],'10.0.3.14':['10.1.0.16','1','eth2'],'10.0.3.15':['10.1.0.31','1','eth2'],'10.0.3.16':['10.1.0.46','1','eth2'],'10.0.3.17':['10.1.0.61','1','eth2'],
                  '10.0.3.18':['10.1.0.76','1','eth2'],'10.0.3.19':['10.1.0.91','1','eth2'],'10.0.3.20':['10.1.0.106','1','eth2'],'10.0.3.21':['10.1.0.121','1','eth2'],'10.0.3.22':['10.1.0.136','1','eth2'],
                  '10.0.3.23':['10.1.0.151','1','eth2'],'10.0.3.24':['10.1.0.166','1','eth2'],
                  '10.0.1.1':['10.1.0.14','14','eth5'],'10.0.1.2':['10.1.0.16','1','eth5'],'10.0.1.3':['10.1.0.31','1','eth5'],'10.0.1.4':['10.1.0.46','1','eth5'],'10.0.1.5':['10.1.0.61','1','eth5'],
                  '10.0.1.6':['10.1.0.76','1','eth5'],'10.0.1.7':['10.1.0.91','1','eth5'],'10.0.1.8':['10.1.0.106','1','eth5'],'10.0.1.9':['10.1.0.121','1','eth5'],'10.0.1.10':['10.1.0.136','1','eth5'],
                  '10.0.1.11':['10.1.0.151','1','eth5'],'10.0.1.12':['10.1.0.167','2','eth5'],
                  '10.0.4.1':['10.1.0.14','14','eth6'],'10.0.4.2':['10.1.0.16','1','eth6'],'10.0.4.3':['10.1.0.31','1','eth6'],'10.0.4.4':['10.1.0.46','1','eth6'],'10.0.4.5':['10.1.0.61','1','eth6'],
                  '10.0.4.6':['10.1.0.76','1','eth6'],'10.0.4.7':['10.1.0.91','1','eth6'],'10.0.4.8':['10.1.0.106','1','eth6'],'10.0.4.9':['10.1.0.121','1','eth6'],'10.0.4.10':['10.1.0.136','1','eth6'],
                  '10.0.4.11':['10.1.0.151','1','eth6'],'10.0.4.12':['10.1.0.167','2','eth6'],
                  '10.1.100.1':['10.1.0.10','1','eth0']}


#set switch to be mirrored
def set_switch_mirroring(switch_IP,mirrored_port,monitoring_port):

    time_lasting_start=time.time()
    print '\r\nPlease wait a minute,it is connecting to the switch...'

    #login to the switch of being set to mirror
    myssh = pxssh.pxssh()
    myssh.login1(server=switch_IP,username=username,password=pwd)

    if ('10.0.3' in switch_IP):
        myssh.sendline('configure')
        time.sleep(0.1)

        print 'Ports mirrored:'
        for c in mirrored_port:
            if c!= int(monitoring_port):
                print 'ge-1/1/'+str(c),
                myssh.sendline('set interface ethernet-switching-options analyzer 1 input egress ge-1/1/'+str(c))
                time.sleep(0.1)
                myssh.sendline('set interface ethernet-switching-options analyzer 1 input ingress ge-1/1/'+str(c))
                time.sleep(0.1)

        print '\r\nport monitoring:\r\n'+'ge-/1/1/'+monitoring_port
        myssh.sendline('set interface ethernet-switching-options analyzer 1 output ge-1/1/'+monitoring_port)
        time.sleep(0.1)

        #commit , exit configure,exit login
        myssh.sendline('commit')
        time.sleep(0.2)
        myssh.sendline('exit')
        time.sleep(0.1)
        myssh.sendline('exit')
        time.sleep(0.1)
    else:
        myssh.sendline('enable')
        time.sleep(0.1)
        myssh.sendline('configure terminal')
        time.sleep(0.1)
        print 'Ports mirrored:'
        for c in mirrored_port:
            if c!= int(monitoring_port):
                print 'ethernet-'+str(c),
                myssh.sendline('monitor session 1 source ethernet '+str(c)+' both')
                time.sleep(0.1)

        print '\r\nport monitoring:\r\n'+'ethernet-'+monitoring_port
        myssh.sendline('monitor session 1 destination ethernet '+monitoring_port)
        time.sleep(0.1)

        #commit , exit configure,exit login
        myssh.sendline('exit')
        time.sleep(0.1)
        myssh.sendline('write')
        time.sleep(0.1)
        myssh.sendline('exit')
        time.sleep(0.1)
    time_lasting_end=time.time()
    print '\r\nIt takes '+str(time_lasting_end-time_lasting_start)+' seconds to set the switch to mirror.\r\n'

    return 1


#delete mirror setting
def delete_switch_mirroring(switch_IP):
    print 'Deleting mirroring configure ... '
    myssh1 = pxssh.pxssh()
    myssh1.login1(server=switch_IP,username=username,password=pwd)
    if ('10.0.3' in switch_IP):
        time.sleep(0.1)
        myssh1.sendline('configure')
        time.sleep(0.1)

        myssh1.sendline('delete interface ethernet-switching-options analyzer 1')
        time.sleep(0.1)
        # simulate input space to check more
        myssh1.sendline('                    ')
        time.sleep(0.1)
        myssh1.sendline('commit')
        time.sleep(0.1)

        myssh1.sendline('exit')
        time.sleep(0.1)
        myssh1.sendline('exit')
        time.sleep(0.1)
    else:
        myssh1.sendline('enable')
        time.sleep(0.1)
        myssh1.sendline('configure terminal')
        time.sleep(0.1)
        myssh1.sendline('no monitor session 1')
        time.sleep(0.1)
        myssh1.sendline('exit')
        time.sleep(0.1)
        myssh1.sendline('write')
        time.sleep(0.1)
        myssh1.sendline('exit')
        time.sleep(0.1)
    return 1

#class of tcpdump process
class MirrorListenprocess(multiprocessing.Process):
    def __init__(self,Listen_address,Listen_time):
        multiprocessing.Process.__init__(self)
        self.Listen_address=Listen_address
        self.Listen_time=Listen_time

    def run(self):
        myssh_listen=pxssh1.pxssh1()
        myssh_listen.login1(server=self.Listen_address,username='xqt',password='xia550505')
        time.sleep(0.1)
        myssh_listen.sendline('sudo python /home/xqt/projectshare/xqt/mirror-data-to-file.py')
        time.sleep(0.1)
        myssh_listen.sendline('xia550505')
        time.sleep(0.1)
        time.sleep(int(self.Listen_time)+25)

    def __del__(self):
        time.sleep(0.1)

#class of tcpdump process
class Deleteprocess(multiprocessing.Process):
    def __init__(self,Delete_address):
        multiprocessing.Process.__init__(self)
        self.Delete_address=Delete_address

    def run(self):
        print '\r\nTerminate this scripts...'
        time.sleep(30)
        myssh_delete=pxssh1.pxssh1()
        myssh_delete.login(server=self.Delete_address,username='xqt',password='xia550505')
        time.sleep(0.1)
        myssh_delete.sendline('python /home/xqt/projectshare/xqt/delete-out-of-date-file.py')

    def __del__(self):
        time.sleep(0.1)


#main function,three parameters should be input by user
if __name__=='__main__':

    print 'usage:mirror -a switch_IP -i mirrored_port -o monitoring_port -t mirror_time \r\n    -a:Pica8 switches,such as 10.0.3.10 \r\n    -i:\r\n        all:mirrored all ports \r\n        1,2,3,...:mirrored ports of 1,2,3,...\r\n        n-m:mirrored ports of n-m\r\n        server_id:ethx:mirror server x:eth x\r\n    -t:\r\n        n:seconds'

    #switch address,input by user
    if sys.argv[1]=='-a':
        switch_IP=sys.argv[2]
        #verify IP is valid, split it,4 of .,every is digit
        '''
             *************************
        '''
    else:
        print 'parameter of switch_IP invalid!'
        exit(1)

    #mirrored port,input by user
    mirrored_port=[]
    if sys.argv[3]=='-i':
        #only one port
        if sys.argv[4].isdigit():
            mirrored_port=[int(sys.argv[4])]
        #all ports
        elif sys.argv[4]=='all':
            mirrored_port=range(1 , 49)
        #continueous ports,a range
        elif '-' in sys.argv[4]:
            temp=sys.argv[4].split('-')
            if temp[0].isdigit() and temp[1].isdigit():
                mirrored_port=range(int(temp[0]) , int(temp[1])+1)
            else:
                print 'parameter of mirrored_port invalid!'
                exit(1)
        #discrete ports,input by user
        elif (',' in sys.argv[4]):
            temp=sys.argv[4].split(',')
            flag_digit=True
            for i in temp:
                if not (i.isdigit()):
                    flag_digit=False
            if flag_digit:
                mirrored_port=temp[:]
            else:
                print 'parameter of mirrored_port invalid!'
                exit(1)
        #server_id and ethx,input by user
        elif(':'in sys.argv[4]):
            temp=sys.argv[4].split(':')
            server_id=int(temp[0])
            port_num_temp=server_id % 15
            if (port_num_temp==0):
                port_num_temp=15
            if (temp[1]=='eth0'):
                mirrored_port=[port_num_temp]
            elif(temp[1]=='eth1'):
                mirrored_port=[24+port_num_temp]
            elif(temp[1]=='eth2'):
                mirrored_port=[port_num_temp]
            elif(temp[1]=='eth3'):
                mirrored_port=[24+port_num_temp]
            elif(temp[1]=='eth5'):
                mirrored_port=[port_num_temp]
            elif(temp[1]=='eth6'):
                mirrored_port=[port_num_temp]

        else:
            print 'parameter of mirrored_port invalid!'
            exit(1)
    else:
        print 'parameter of mirrored_port invalid!'
        exit(1)

    '''
    if sys.argv[5]=='-o':
        monitoring_port=sys.argv[6]
        #verify whether argv[6] is valid port
    else:
        print 'parameter of monitoring_port invalid!'
        exit(1)
    '''
    #monitoring ports,set by global parameter
    monitoring_port=dict_switch_host[switch_IP][1]

    #monitoring time,input by user
    if sys.argv[5]=='-t':
        if sys.argv[6].isdigit():
            mirror_time=int(sys.argv[6])
        else:
            print 'parameter of time invalid'
            exit(1)
    else:
        print 'No parameter of time!'
        exit(1)

    #call function of set_switch_mirroring to set switch to mirror
    if ('10.0.3.' in switch_IP):
        username='admin'
        pwd='pica8'
    else:
        username='admin'
        pwd='admin'

    #start a process,let remote server to run mirror-data-to-file.py
    p=MirrorListenprocess(dict_switch_host[switch_IP][0],mirror_time)
    p.start()


    #set switch to be mirroring
    set_switch_mirroring(switch_IP,mirrored_port,monitoring_port)


    print '\r\nstart of mirror!\r\n'
    print 'Mirrored data is directed to the host of '+dict_switch_host[switch_IP][0]+'\r\n'
    #send message to the host attached to the mirrored switch, let the host to collect data and save it.
    port= 8089
    host=dict_switch_host[switch_IP][0]
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto('_switch_'+switch_IP+'_mirroredport_'+sys.argv[4]+'_monitoringport_'+monitoring_port+' '+str(mirror_time)+' '+dict_switch_host[switch_IP][2],(host,port))

    #let the host terminate at first.then after 2 seconds, this program  will stop
    time.sleep(mirror_time+2)

    print '\r\nend of this mirror!\r\n'

    #call function of delete_switch_mirroring to delete mirroring setting
    delete_switch_mirroring(switch_IP)
    print 'Completed the deletion of switch mirroring setting.'

    #copy mirrored file to local directory
    print '\r\nBegin to copy mirrored file to local directory:\r\n'
    os.system('scp xqt@'+dict_switch_host[switch_IP][0]+':/home/xqt/projectshare/mirrorfiles/*.* ./')

    #delete files on the mirrored server
    #p_delete=Deleteprocess(dict_switch_host[switch_IP][0])
    #p_delete.start()












