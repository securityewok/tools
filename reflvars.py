#Grab all js vars from site, try each one as a get parameter to see if they're processed and reflected for whatever reason

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import argparse


def get_vars(url, cookies={}, proxy="None", headers={}):
    if proxy != "None":
	proxies = {'http': proxy, 'https': proxy}
    	response = requests.get(url, cookies=cookies, timeout=10, verify=False, proxies=proxies, headers=headers)
    else:
	response = requests.get(url, cookies=cookies, timeout=10, verify=False, headers=headers)
    print "[+] Received response: " + str(response.status_code)
    print "[+] Gettings vars..."
    pattern = 'var [^=;]+'
    vars_array = re.findall(pattern, response.text)
    if len(vars_array) == 0:
        print "No vars found"
        sys.exit(0)
    vars_array_after = []
    for v in vars_array:
        if "," in v:
	    for z in v.split(','):
		if "var" in z:
                    vars_array_after.append(z.split(" ")[1])
		else:
		    vars_array_after.append(z)
	else:
	    vars_array_after.append(v.split(' ')[1])
    find_refl(url, vars_array_after, cookies, proxy, headers)

def find_refl(url, params, cookies={}, proxy="None", headers={}):
    refl = "tr01"
    for p in params:
        if "?" not in url:
	    n_url = url+"?"+p+"="+refl
	else:
            n_url = url+"&"+p+"="+refl
        if proxy != "None":
            proxies = {'http': proxy, 'https': proxy}
	    response = requests.get(n_url, cookies=cookies, timeout=10, verify=False, proxies=proxies, headers=headers)
	else:
            response = requests.get(url, cookies=cookies, timeout=10, verify=False, headers=headers)
	if refl in response.text:
            print "[!] Reflective value found for parameter: " + p

def main():
    parser = argparse.ArgumentParser(description="Test js vars for reflection")
    parser.add_argument('-url', type=str, help="Insert url", default="None")
    parser.add_argument('-cookie', type=str, help="Insert session values 'name:value'")
    parser.add_argument('-proxy', type=str, help="Insert proxy 'eg. https://127.0.0.1:8080'")
    args = parser.parse_args()
    if args.url != "None":
        if args.cookie != "None":
            cookies = {args.cookie.split(":")[0]:args.cookie.split(":")[1]}
            get_vars(args.url, cookies, args.proxy)
    else:
	print "Provide url"

main()

