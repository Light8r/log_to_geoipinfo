import re
import requests
import json

api_url = "https://ipgeolocation.abstractapi.com/v1/"
api_key = ""
def get_geolocation_info(validated_ip_address):
    url = "https://ipgeolocation.abstractapi.com/v1"
    querystring = {"api_key": api_key, "ip_address": validated_ip_address}
    try:
        response = requests.request("GET", url, params=querystring)
        return response.content
    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Geolocation API: {api_error}")
        raise SystemExit(api_error)

f=open("nohup.out")
line=f.readline()
ip_list=[]
while line:
    flag=line.find("remote_ip")
    if flag !=-1:
        keyip_group=re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",line)
        keyip=keyip_group[0]
        if keyip not in ip_list:
            ip_list.append(keyip)
    line=f.readline()
f.close()
ip_list=sorted(ip_list)
content_group=[]
for item in ip_list:
    content_group.append(get_geolocation_info(item))
f2=open('out.json','w',encoding='utf-8')
for item in content_group:
    itemtmp=item.decode("utf8").replace("'",'"')
    data=json.dumps(itemtmp,indent=4,sort_keys=True)
    f2.write(itemtmp+'\r\n')
f2.close()
