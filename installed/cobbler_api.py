# -*- coding: utf-8 -*-
import xmlrpclib

class CobblerAPI(object):
    def __init__(self,url,user,password):
        self.cobbler_user = user
        self.cobbler_pass = password
        self.cobbler_url = url

    def add_system(self,hostname,ip_add,mac_add,profile):
        '''
        添加cobble系统信息
        :param hostname:
        :param ip_add:
        :param mac_add:
        :param profile:
        :return:
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        hostname = '_'.join(hostname.split())
        remote = xmlrpclib.Server(self.cobbler_url)
        token = remote.login(self.cobbler_user,self.cobbler_pass)
        system_id = remote.new_system(token)
        remote.modify_system(system_id,"name",hostname,token)
        remote.modify_system(system_id,"hostname",hostname,token)
        remote.modify_system(system_id,'modify_interface',{
            "macaddress-eth0" : mac_add,
            "ipaddress-eth0" : ip_add,
            "dnsname-eth0" : hostname,
        }, token)
        remote.modify_system(system_id,"profile",profile,token)
        remote.save_system(system_id, token)
        try:
            remote.sync(token)
            ret['comment'].append(' add system success')
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret

def main():
    cobbler = CobblerAPI(url='http://ip/cobbler_api',user='cobbler',password='cobbler',)
    ret = cobbler.add_system()
    print ret

if __name__ == '__main__':
    main()