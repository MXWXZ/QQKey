import requests
import re


class QQLogin:
    def __init__(self):
        self.session = None      # login session
        self.headers = {
            'Host': 'localhost.ptlogin2.qq.com:',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.port = None         # listen port
        self.qqnumber = None     # qqnumber
        self.nickname = None     # nickname

    '''
    Get QQ account
    @return     true for get success
    '''

    def GetAccount(self):
        self.session = requests.Session()
        self.session.cookies.set('pt_user_id','123456789012345678', domain='ptlogin2.qq.com')
        self.session.cookies.set('pt_login_sig','abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl', domain='ptlogin2.qq.com')
        self.session.cookies.set('pt_clientip','1234567890123456', domain='ptlogin2.qq.com')
        self.session.cookies.set('pt_serverip','1234567890123456', domain='ptlogin2.qq.com')
        self.session.cookies.set('pt_local_token','1234567890', domain='ptlogin2.qq.com')
        self.session.cookies.set('uikey','abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl', domain='ptlogin2.qq.com')
        self.session.cookies.set('pt_guid_sig','abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl', domain='ptlogin2.qq.com')
        self.session.cookies.set('ptui_identifier','abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd', domain='ui.ptlogin2.qq.com')
        self.session.cookies.set('pgv_pvi', '1234567890', domain='ptlogin2.qq.com')
        self.session.cookies.set('pgv_si', 's1111111111', domain='ptlogin2.qq.com')
        ret = False
        for self.port in range(4300, 4309):     # qq local server
            try:
                self.headers['Host'] = 'localhost.ptlogin2.qq.com:' + str(self.port)
                req = self.session.get('https://localhost.ptlogin2.qq.com:'+str(self.port) +
                                       '/pt_get_uins?callback=ptui_getuins_CB&r=0.9899515903716838&pt_local_tk=' +
                                       self.session.cookies['pt_local_token'], headers=self.headers)
                self.qqnumber = re.search(r'uin":"([0-9]*)"', req.text).group(1)
                self.nickname = re.search(r'nickname":"(.*?)"', req.text).group(1)

                self.session.get('https://localhost.ptlogin2.qq.com:'+str(self.port)+'/pt_get_st?clientuin='+self.qqnumber +
                                '&callback=ptui_getst_CB&r=0.9899515903716838&pt_local_tk='+self.session.cookies['pt_local_token'], headers=self.headers)
                ret = True
                break
            except:
                continue
        return ret

    '''
    Get qzone login key
    @return     login key, None for error
    '''

    def LoginQzone(self):
        return self.__Login('pt_aid=549000912&daid=5&u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone')

    '''
    Get qmail login key
    @return     login key, None for error
    '''
    def LoginQmail(self):
        return self.__Login('pt_aid=522005705&daid=4&u1=https%3A%2F%2Fmail.qq.com%2Fcgi-bin%2Freadtemplate%3Fcheck%3Dfalse%26t%3Dloginpage_new_jump%26vt%3Dpassport%26vm%3Dwpt%26ft%3Dloginpage%26target%3D')
    
    '''
    Universe login method
    '''
    def __Login(self,url):
        try:
            self.session.get('https://localhost.ptlogin2.qq.com:'+str(self.port)+'/pt_get_st?clientuin='+self.qqnumber +
                                '&callback=ptui_getst_CB&r=0.9899515903716838&pt_local_tk='+self.session.cookies['pt_local_token'], headers=self.headers)
            self.headers['Host'] = 'ssl.ptlogin2.qq.com'
            req = self.session.get('https://ssl.ptlogin2.qq.com/jump?clientuin='+self.qqnumber +
                                    '&keyindex=9&'+url+'&pt_local_tk=' +self.session.cookies['pt_local_token']+'&pt_3rd_aid=0&ptopt=1&style=40', headers=self.headers)
            return re.search(r"_CB\('0', '(.*?)'", req.text).group(1)
        except:
            return None


if __name__ == '__main__':
    obj = QQLogin()
    obj.GetAccount()
    print('QQKey:' + obj.session.cookies.get_dict()['clientkey']+'\n')
    print('Cookie: ' + ('; '.join(['='.join(item) for item in obj.session.cookies.get_dict().items()])))
    if(input('Auto get url?(y/n)')=='y'):
        print('Qzone:')
        print(obj.LoginQzone())
        print('Qmail:')
        print(obj.LoginQmail())