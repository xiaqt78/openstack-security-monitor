__author__ = 'root'
import libvirt
import time




#conn=libvirt.openReadOnly('qemu+ssh://xqt@10.1.0.152/system')
dic={'a':'fdsa'}
print dic
conn=libvirt.open('qemu+tcp://10.1.0.002/system')
names=conn.listDomainsID()
print len(names)
for item in names:
    p=conn.lookupByID(item)
    print p.UUIDString()  #obtain uuid
    print p.name()     #obtain name
    print p.info()
    print p.XMLDesc()
    print p.state()


    print '--------------------------------------\r\n\r\n'

    if item==13:
        p.suspend()
        time.sleep(5)
        p.resume()

    #p.suspend() #stop
    #time.sleep(2)
    #p.resume()
    #p.destroy() destroy self






conn.close()