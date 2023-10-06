import requests, json, time, datetime, sys,os

api_url = "https://ipgeolocation.abstractapi.com/v1/"
api_key = sys.argv[1]
connection_analysis = {}
HOST_NUMBER = 10


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
    data = json.loads(line)
    request = data['request']
    remote_ip = request['remote_ip']
    timestamp = data['ts']
    host = request['host']
    if remote_ip not in connection_analysis:
        ipdata = json.loads(get_geolocation_info(remote_ip))
        time.sleep(1)
        city = ipdata['city']
        country = ipdata['country']
        connection = ipdata['connection']
        isp_name = connection['isp_name']
        connection_type = connection['connection_type']
        host_analysis = {host: 1}
        ipinfo = {'time': time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime(timestamp))),
                  'host_analysis': host_analysis,
                  'city': city,
                  'country': country,
                  'isp_name': isp_name,
                  'connection_type': connection_type
                  }
        connection_analysis[remote_ip] = ipinfo
    else:
        ipinfo = connection_analysis[remote_ip]
        ipinfo['time'] = time.strftime("%Y-%m-%d %H:%M:%S", (time.localtime(timestamp)))
        host_analysis = ipinfo['host_analysis']
        if host not in host_analysis:
            host_analysis.setdefault(host, 1)
        else:
            host_analysis[host] += 1
        ipinfo['host_analysis'] = host_analysis
        connection_analysis[remote_ip] = ipinfo
    line = fileopen.readline()
for ip, analysis in connection_analysis.items():
    host_analysis = analysis['host_analysis']
    plist = sorted(host_analysis.items(), key=lambda x: (x[1], x[0]), reverse=True)
    plist = plist[:min(HOST_NUMBER, len(host_analysis))]
    tmp = {}
    for item in plist:
        tmp[item[0]] = item[1]
    host_analysis = tmp
    analysis['host_analysis'] = host_analysis
    connection_analysis[ip] = analysis
Output = json.dumps(connection_analysis, sort_keys=True, indent=4, separators=(',', ':'))
fileout = open("out.json", "w", encoding="utf-8")
fileout.write(Output)
fileout.close()
os.rename("out.json", time.strftime("%Y_%m_%d_%H_%M_%Sipanalysis.json"))
if len(connection_analysis)!=0:
    print("Your ip has been successfully converted to GeoIpLocation into Dateipanalysis.json")
else:
    print("No ip found in log file!")
