import requests
import json
import pandas as pd


def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude:
                    flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out


# 定义URL
url = "https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=100&offset=0&companyName=companies%2Fd475e46c-52e0-4b9b-a525-48027b002583&customAttributeFilter=ats_portalid%3D%22SuccessFactors%22&orderBy=posting_publish_time%20desc&disableSpellCheck=true&enableBroadening=true"
nextpagetoken = ''

# 发送GET请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'NextPageToken': nextpagetoken
}
response = requests.get(url, headers=headers)
# 解释requests.get
# requests.get(url, params=None, **kwargs)
# url : URL for the new Request object.
# params : (optional) Dictionary or bytes to be sent in the query string for the Request.
# **kwargs : Optional arguments that request takes.
# 返回的是一个response对象
# response.text返回的是一个str对象
# response.content返回的是一个bytes对象
# response.json返回的是一个json对象


# 从响应内容中删除"jobsCallback("和最后的")"，然后解析JSON数据


data = json.loads(response.text[13:-1])

nextpagetoken = data['nextPageToken']
print(nextpagetoken)

'''
if nextpagetoken != '':
    url = "https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=100&offset=100&companyName=companies%2Fd475e46c-52e0-4b9b-a525-48027b002583&customAttributeFilter=ats_portalid%3D%22SuccessFactors%22&orderBy=posting_publish_time%20desc&disableSpellCheck=true&enableBroadening=true"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'NextPageToken': nextpagetoken
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text[13:-1])

data = json.loads(response.text[13:-1])

nextpagetoken = data['nextPageToken']
print(nextpagetoken)

'''
# 将数据写入本地JSON文件
with open("page.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
