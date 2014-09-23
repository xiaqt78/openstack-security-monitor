__author__ = 'root'
# coding=utf-8

import novaclient.v3.client as nvclient
import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
import libvirt
from xml.dom.minidom import parseString
import pxssh
import time

#global parameters
#parameters of username and password for physical host
physical_host_username='xqt'
physical_host_pwd='xia550505'
#parameters for openstack
oenstack_username='xqt'
openstack_pwd='xia550505'
openstack_project_tenant_id='xqt'
openstack_ip='10.1.1.250'
#parameters for monitoring security_vm
security_vm_name1='detect'
security_vm_name2='security'
security_vm_name3='engine'
security_vm_name4='xxxxxxxxxx'

print '**********************************************************************************************************************'
print '*                                                                                                                    *'
print '*             Main function: remove monitoring function of security_vm runing on physical host                       *'
print '*                                 developed by XiaQingtang 2014-08-10                                                *'
print '*                              system group of IIIS Tsinghua University                                              *'
print '*                                                                                                                    *'
print '**********************************************************************************************************************'
print '\r\n'
print 'getting parameters of security_vm from openstack ... ...'
#connect to openstack to collect info of security_vm for every physical hostS
nt = nvclient.Client(auth_url='http://'+openstack_ip+':5000/v2.0/',username=oenstack_username,password=openstack_pwd,project_id=openstack_project_tenant_id,service_type='compute')
servers=nt.servers.list()#获取所有虚拟机的列表
dic_to_be_mirrored_host={}#存储物理机上运行的所有虚拟机，键：物理机IP，值：是个列表，列表的值是元组，元组包括两部分：UUID和instance name
dic_to_be_mirrored_host_name={}#存储物理机上运行的所有虚拟机，键：物理机IP，值：是个列表，列表的值是虚拟机的openstack名字
for serv_item in servers:
    dic_s=serv_item._info#获取虚拟机的info，是个字典，包含了各种信息
    strname=serv_item.name#获取虚拟机在openstack中的名字
    if (strname.find(security_vm_name1)>-1)or(strname.find(security_vm_name2)>-1)or(strname.find(security_vm_name3)>-1):#监控虚拟机在openstack中包含这些词组
        struuid=dic_s['id']#UUID
        strinstancename=dic_s['OS-EXT-SRV-ATTR:instance_name']
        strhostname=dic_s['OS-EXT-SRV-ATTR:host']#hostname
        if (strhostname[1]=='0')and(strhostname[2]=='0'):
            strhostname_temp=strhostname[2]
        elif(strhostname[1]=='0')and(strhostname[2]<>'0'):
            strhostname_temp=strhostname[2:]
        else:
            strhostname_temp=strhostname[1:]
        strhostip='10.1.0.'+strhostname_temp
        if strhostip in dic_to_be_mirrored_host:#当前虚拟机不是所在物理机的第一个，则当前虚拟机的信息追加到字典dic_to_be_mirrored_host和第二个字典
            dic_to_be_mirrored_host[strhostip].append((struuid,strinstancename))
            dic_to_be_mirrored_host_name[strhostip].append(strname)
        else:#当前虚拟机是所在物理机的第一个，字典的值：列表初始化，然后添加
            dic_to_be_mirrored_host[strhostip]=[]
            dic_to_be_mirrored_host_name[strhostip]=[]
            dic_to_be_mirrored_host[strhostip].append((struuid,strinstancename))
            dic_to_be_mirrored_host_name[strhostip].append(strname)
#print dic_to_be_mirrored_host_name
#print dic_to_be_mirrored_host
#for each physical host to collect the bridge info of security_vm running on it
dic_mirror_host_bridge_mac={}#存储物理机上进行监控的虚拟机的bridge、mac、openstack上的VM_name
for key in dic_to_be_mirrored_host:
    #print (dic_to_be_mirrored_host[key])
    conn=libvirt.open('qemu+tcp://'+key+'/system')
    vms=conn.listDomainsID()
    for item in vms:
        vm=conn.lookupByID(item)
        #print vm.UUIDString(),vm.name()
        if dic_to_be_mirrored_host[key].count((vm.UUIDString(),vm.name()))>0:#如果当前虚拟机在物理机的监控虚拟机列表中，就选当前虚拟机为该物理机的监控服务器
            i=dic_to_be_mirrored_host[key].index((vm.UUIDString(),vm.name()))#当前物理机虚拟机列表中对应于该符合要求的虚拟机的索引
            #if key=='10.1.0.002':
                #print(vm.XMLDesc())
            #print(vm.name(),key)
            list_bridge=[]
            list_mac=[]
            #从该虚拟机的XML配置文件中查找bridge、mac值
            doc = parseString(vm.XMLDesc())
            for source in doc.getElementsByTagName('source'):
                #print source.getAttribute('bridge')
                if source.getAttribute('bridge')!='':
                    list_bridge.append(source.getAttribute('bridge'))
            for mac in doc.getElementsByTagName('mac'):
                #print mac.getAttribute('address')
                if mac.getAttribute('address')!='':
                    list_mac.append(mac.getAttribute('address'))
            dic_mirror_host_bridge_mac[key]=[]
            #print dic_to_be_mirrored_host[key][i]
            if (len(list_bridge)>1) and (len(list_mac)>1):#多个网卡的，选择第二块卡接收镜像数据
                dic_mirror_host_bridge_mac[key].append((list_bridge[1],list_mac[1],dic_to_be_mirrored_host_name[key][i]))
            else:
                dic_mirror_host_bridge_mac[key].append((list_bridge[0],list_mac[0],dic_to_be_mirrored_host_name[key][i]))
            break#一台物理机上就选择一个符合条件的虚拟机进行安全监控

    conn.close()
print 'success getting info of security_vm.\r\n'

for key in dic_mirror_host_bridge_mac:
    print '\r\n... ... monitoring setting of host '+key+' will be removed ... ...\r\nconnecting to physical host '+key+'.please wait a minute ... ...'
    myssh = pxssh.pxssh()
    if key=='10.1.0.5' or key=='10.1.0.2':
        myssh.login(server=key,username='root',password='root123')
    else:
        myssh.login(server=key,username=physical_host_username,password=physical_host_pwd)
    mirrored_port=str(dic_mirror_host_bridge_mac[key][0][0][3:])
    #print key,mirrored_port
    print 'sending mirror clear command to physical host '+key+' ... ...'
    command='sudo ovs-vsctl -- clear bridge br-int mirrors'
    myssh.sendline(command)
    time.sleep(0.5)
    print 'sending brctl command to physical host n'+key[-3:]+' ... ...'
    myssh.sendline('sudo brctl setageing qbr'+mirrored_port+' 15')
    time.sleep(0.5)
    #print command
    print 'completed setting.'
    myssh.close()
