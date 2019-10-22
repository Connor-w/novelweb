from django.test import TestCase
import requests
import ssl

# Create your tests here.

ssl._create_default_https_content=ssl._create_unverified_context

url='https://fanyi.baidu.com/sug'

data={
    'kw':'dog'
}

header= {
    'UserAgent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

response=requests.post(url=url,data=data)

import json
print(type(response.text),response.text)
a=json.loads(response.text)
b=a['data']
print(json.loads(response.text))
for i in b:
    print(i)