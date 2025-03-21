import os,base64,requests
alypaccountslist=[]
with open('alyp.txt',encoding='utf-8',errors='ignore') as alypaccounts:
    for index,alypaccountdata in enumerate(alypaccounts,1):
        values=alypaccountdata.strip().split('#')
        remark,alypaccount=values[0],values[1]
        print('========账号%s：%s========'%(index,remark))
        print('正在获取accesstoken...')
        resp=requests.post('https://auth.aliyundrive.com/v2/account/token',json={'refresh_token':alypaccount,'grant_type':'refresh_token'}).json()
        code=resp.get('code','')
        if code:
            print('获取accesstoken失败：%s'%code)
        else:
            accesstoken,refreshtoken=resp['access_token'],resp['refresh_token']
            alypaccountslist.append('%s#%s'%(remark,refreshtoken))
            print('开始签到...')
            resp=requests.post('https://member.aliyundrive.com/v1/activity/sign_in_list',json={},headers={'Authorization':accesstoken}).json()
            message=resp['message']
            if message:
                print('签到失败：%s'%message)
            else:
                print('签到成功：本月已连续签到%s天'%resp['result']['signInCount'])
print('正在刷新refreshtoken...')
with open('alyp.txt','w',encoding='utf-8',errors='ignore') as f:
    for alypaccountdata in alypaccountslist:
        f.write('%s\n'%alypaccountdata)
print('刷新refreshtoken成功')
