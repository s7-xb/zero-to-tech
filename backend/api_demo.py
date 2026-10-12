import requests
resp = requests.get("http://httpbin.org/ip")
print(resp.json())
