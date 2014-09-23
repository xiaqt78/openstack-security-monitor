__author__ = 'root'
import novaclient.v3.client as nvclient
#import quantumclient.v2_0.client as qtclient
import  pxssh
'''
def print_values(val, type):
    if type == 'ports':
        val_list = val['ports']
    if type == 'networks':
        val_list = val['networks']
    if type == 'routers':
        val_list = val['routers']
    for p in val_list:
        for k, v in p.items():
            print("%s : %s" % (k, v))
        print('\n')


def print_values_server(val, server_id, type):
    if type == 'ports':
        val_list = val['ports']
    if type == 'networks':
        val_list = val['networks']
    for p in val_list:
        bool = False
        for k, v in p.items():
            if k == 'device_id' and v == server_id:
                bool = True
        if bool:
            for k, v in p.items():
                print("%s : %s" % (k, v))
            print('\n')


nt = qtclient.Client(auth_url='http://10.1.0.2:5000/v2.0/',username='xqt',password='xia550505',project_id='admin',service_type='networks')
net=nt.list_networks
print_values(net, 'networks')
'''
myssh=pxssh.pxssh()
myssh.login(server='10.1.0.002',username='root',password='root123')
myssh.sendline('ls -l')
myssh.close()