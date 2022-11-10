from util import *
import requests
import time
import re
import json
ss=requests.Session()
versionId="0.0.0.0"#目前是这么个玩意
sourceFrom="wap"#很容易猜
osv="windows 10"#没必要写说明吧
page="1"#这种不需要解释吧
pageSize="10"#自己多试试 有惊喜
city_filter="12"#城市么多试试
city="12"#一样是城市没换过
guazi_city="12"#瓜子城市,感觉有自己定义方式
tag_types="10012"#10012是必看好车,其他么自己猜猜试试
platfromSource="wap"#感觉不需要解释



rsp1=ss.get(r'https://www.guazi.com/')#没必要讲解吧,就是交换个cookie
rsp2=ss.get(rf'https://mapi.guazi.com/car-source/option/font?versionId={versionId}&sourceFrom={sourceFrom}&osv={osv}&platfromSource={platfromSource}')#获取字体文件URL
json1={
}
try:
    json1=rsp2.json()#确认下是否能获取json
except:
    json1={}
assert 'code' in json1.keys() and 'data' in json1.keys() and 'url' in json1['data'] and json1['code']==0 and 'message' in json1.keys() and json1['message']=='成功'
font_url=rsp2.json()['data']['url']
rsp3=ss.get(font_url)
temptext=str(int(time.time()*(10**7)))
open(temptext,'wb').write(rsp3.content)
d=getDict(temptext)
dataurl=rf'https://mapi.guazi.com/car-source/carList/pcList?versionId={versionId}&sourceFrom={sourceFrom}&osv={osv}&page={page}&pageSize={pageSize}&city_filter={city_filter}&city={city}&guazi_city={guazi_city}&tag_types={tag_types}&platfromSource={platfromSource}'
rsp3=ss.get(dataurl)#获取置换过的数据

resjson={
}
try:
    resjson=rsp3.json()#确认下是否能获取json
except:
    resjson={}



assert 'code' in resjson.keys() and 'data' in resjson.keys() and 'message' in resjson.keys() and resjson['message']=='成功' and resjson['code']==0


str1=rsp3.text

resstr=re.sub(r'&#(\d{1,5});',lambda x:d['uni'+ hex(int(x.groups()[0]))[2:]]['char'] if x and x.group() else '',str1)

open(rf'{temptext}.json','w').write(resstr)
if os.path.exists(temptext):
  os.remove(temptext)