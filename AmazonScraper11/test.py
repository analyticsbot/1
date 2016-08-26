import requests
auth = requests.auth.HTTPProxyAuth('manutd0707', 'vbym5o5r80uvaer')
proxies = {'http': 'http://us-fl.proxymesh.com:31280'}
response = requests.get('http://icanhazip.com', proxies=proxies, auth=auth)
print response.text
