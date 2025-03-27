import os,sys,base64,requests,traceback

mdhy=os.getenv('mdhy')
mdhyaccounts=mdhy.split('@')
for index,mdhyaccountdata in enumerate(mdhyaccounts,1):
    values=mdhyaccountdata.split('#')
    remark,mdhyaccount=values[0],values[1]
    print('========账号%s：%s========'%(index,remark))
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) XWEB/9129','apiKey':'3660663068894a0d9fea574c2673f3c0','ucAccessToken':mdhyaccount}
    resp=requests.post('https://mvip.midea.cn/mscp_mscp/api/cms_api/activity-center-im-service/im-svr/im/game/page/sign',headers=headers,json={'restParams':{'actvId':'401671388248692763','rootCode':'MDHY','appCode':'MDHY_XCX'}}).json()
    if resp['code']=='000000':
        data=resp['data']
        if data['result']:
            print('每日签到：%s'%data['dailyRewardInfo']['name'])
        else:
            print('每日签到：已完成')
    else:
        print('每日签到：%s'%resp['msg'])
