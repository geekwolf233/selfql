import os,re,ast,sys,base64,requests,traceback

xclx=os.getenv('xclx')
xclxaccounts=xclx.split('@')
for index,xclxaccountdata in enumerate(xclxaccounts,1):
    values=xclxaccountdata.split('#')
    remark,xclxaccount=values[0],values[1]
    print('========账号%s：%s========'%(index,remark))
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c33)XWEB/11581','cookie':xclxaccount}
    print('=====每日签到=====')
    resp=requests.post('https://m.ctrip.com/restapi/soa2/22769/signToday',headers=headers,json={'openId':''}).json()
    message=resp['message']
    if message=='SUCCESS':
        print('每日签到：+%s积分'%resp['baseIntegratedPoint'])
    else:
        print('每日签到：%s'%message)
    for channelCode in ['2H3294O46M','JR442JH832']:
        resp=requests.post('https://m.ctrip.com/restapi/soa2/22598/userTaskList',headers=headers,json={'channelCode':channelCode,'version':'3'}).json()
        projectName,todoTaskList=resp['projectName'],resp['todoTaskList']
        print('=====%s任务====='%projectName)
        if todoTaskList:
            for tasklist in todoTaskList:
                taskid,displayName,eventType,h5Url,eventCondition=tasklist['id'],tasklist['displayName'],tasklist['eventType'],tasklist['h5Url'],tasklist['eventCondition']
                resp=requests.post('https://m.ctrip.com/restapi/soa2/22598/todoTask',headers=headers,json={'channelCode':channelCode,'taskId':taskid,'status':0,'done':0}).json()
                message=resp['message']
                if message=='SUCCESS':
                    print('%s-领任务：已完成'%displayName)
                else:
                    print('%s-领任务：%s'%(displayName,message))
                if eventType=='NO_REPEAT_BROWSE':
                    resp=requests.post('https://m.ctrip.com/restapi/soa2/22598/taskBrowseDone',headers=headers,json={'_taskDetailId':h5Url,'_mktTaskActivityId':ast.literal_eval(eventCondition)['_mktTaskActivityId']}).json()
                    message=resp['message']
                    if message=='SUCCESS':
                        print('%s-做任务：已完成'%displayName)
                    else:
                        print('%s-做任务：%s'%(displayName,message))
                else:
                    resp=requests.post('https://m.ctrip.com/restapi/soa2/22598/todoTask',headers=headers,json={'channelCode':channelCode,'taskId':taskid,'status':1,'done':1}).json()
                    message=resp['message']
                    if message=='SUCCESS':
                        print('%s-做任务：已完成'%displayName)
                    else:
                        print('%s-做任务：%s'%(displayName,message))
                resp=requests.post('https://m.ctrip.com/restapi/soa2/22598/awardTask',headers=headers,json={'channelCode':channelCode,'taskId':taskid}).json()
                message=resp['message']
                if message=='SUCCESS':
                    print('%s-领奖励：%s'%(displayName,resp['awardDesc']))
                else:
                    print('%s-领奖励：%s'%(displayName,message))
        else:
            print('%s任务：已完成'%projectName)
    print('=====领酒店神券=====')
    promotionIds=[]
    resp=requests.post('https://m.ctrip.com/restapi/soa2/23150/GetCouponsAndRewardsInfo.json',headers=headers,json={'eventPinyins':['liuliangzhendiqitaquanbao']}).json()
    for couponDetailInfo in resp['couponDetailInfos']:
        promotionIds.append(couponDetailInfo['promotionId'])
    resp=requests.post('https://m.ctrip.com/restapi/soa2/23150/ReceiveCouponsAndRewards.json',headers=headers,json={'eventPinyin':'liuliangzhendiqitaquanbao','promotionIds':promotionIds}).json()
    couponResults=resp['couponResults']
    if len(couponResults)==1:
        msg=couponResults[0]['result']['msg']
        if 'msg' in msg:
            msg=re.findall(r'"msg":"(.+)"',msg)[0]
        print('领券结果：%s'%msg)
    else:
        for couponResult in couponResults:
            msg=couponResult['result']['msg']
            if 'msg' in msg:
                msg=re.findall(r'"msg":"(.+)"',msg)[0]
                print('领券结果：%s'%msg)
            else:
                print('领券结果：%s'%couponResult['couponName'])
