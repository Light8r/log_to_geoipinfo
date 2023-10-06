import re, requests, json, sys

api_url = "https://ipgeolocation.abstractapi.com/v1/"
api_key = sys.argv[1]
content_group = []
ip_list = []


def get_geolocation_info(validated_ip_address):
    querystring = {"api_key": api_key, "ip_address": validated_ip_address}
    try:
        response = requests.request("GET", api_url, params=querystring)
        return response.content
    except requests.exceptions.RequestException as api_error:
        print(f"There was an error contacting the Geolocation API: {api_error}")
        raise SystemExit(api_error)


fileopen = open("naive.log")
line = fileopen.readline()
while line:
    flag = line.find("remote_ip")
    if flag != -1:
        ipfounded = re.search(
            r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", line[flag:-1])
        if ipfounded.group() not in ip_list:
            ip_list.append(ipfounded.group())
    line = fileopen.readline()
fileopen.close()

ip_list.sort()
for item in ip_list:
    data = json.loads(get_geolocation_info(item))
    try:
        ip = data['ip_address']
        city = data['city']
        content_group.append(ip + ' : ' + city)
    except KeyError:
        content_group.append(item+" : No data")
for item in content_group:
    outfile = open("out.txt", "w")
    print(item)
    outfile.write(item)
    outfile.close()
if len(content_group)!=0:
    print("Your ip has been successfully converted to GeoIpLocation into out.txt")
else:
    print("No ip found in log file!")
