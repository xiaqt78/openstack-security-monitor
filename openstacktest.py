__author__ = 'root'

import keystoneclient.v2_0.client as ksclient
import novaclient.v3.client as nvclient

# Replace the values below  the ones from your local config,
auth_url = "http://10.1.0.2:35357/v2.0"
username = "admin"
password = "admin"
tenant_name = "admin"

keystone = ksclient.Client(auth_url=auth_url, username=username,
                           password=password, tenant_name=tenant_name)
print keystone.auth_token
print keystone.tenant_id

nova = nvclient.servers(auth_url='http://10.1.0.2:8774',username=username,password=password,auth_token=keystone.auth_token)
