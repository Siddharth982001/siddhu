import json
import requests
from bs4 import BeautifulSoup
import dateutil.parser

def smeexpress(tracking_number):
 url = "http://customer.smexpresslogistics.com:7080/IYANA/webTrackYourConsignmentAction.do?reqCode=showTrackYourCosignmentPage&searchType=AWBNO&searchValue=6010857441"
 payload = f"reqCode=showTrackYourCosignmentPage&searchType=AWBNO&searchValue={tracking_number}"
 headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Content-Type': 'text/plain',
  'Cookie': 'JSESSIONID=E1C2FAD4BE14C148574C2C7FD1812A48'}
 response = requests.request("GET", url, headers=headers, data=payload)
 resp=response.text
 soup=BeautifulSoup(resp,'html.parser')
 table=soup.find('table',class_='dtable')
 tr=table.find_all('tr')
 datalist=[]
 for i in tr:
    if i==tr[0]:
        pass
    else:
        td=i.find_all('td')
        date=td[2].text
        date=dateutil.parser.parse(date,dayfirst=True).strftime('%Y-%m-%dT%H:%M:%S')
        message=td[1].text
        if "AT" in message:
            message=message.split('AT')
        elif "FOR" in message:
            message=message.split(' FOR')
        elif "TO" in message:
            message=message.split('TO')
        elif " " in message:
            message=message.split()
        city=message[1]
        message=message[0]
        message=message.split()
        message=message[3]
        if " DELIVERED " in message:
            _tag=" DELIVERED "
        elif 'BOOKED' in message:
            _tag='InfoReceived'
        else:
            _tag='InTransist'
        data_dict = {
            "zip": None,
            "country_iso3": None,
            "slug": "SMEXPRESS",
            "state": None,
            "code": None,
            "coordinates": [],
            "message": message,
            "city":city or '',
            "tag":_tag or  '',
            "created_at": "",
            "checkpoint_time": date,
            "pod_link": '',
            "edd":""
        }
        datalist.append(data_dict)
 return datalist

if __name__=='__main__':
    datalist=smeexpress('6010857441')
    print(json.dumps(datalist,indent=4))