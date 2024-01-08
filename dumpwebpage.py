import requests
import json

# 定义URL
url = "https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=1000&offset=0&companyName=companies%2Fd475e46c-52e0-4b9b-a525-48027b002583&customAttributeFilter=ats_portalid%3D%22SuccessFactors%22&orderBy=posting_publish_time%20desc&disableSpellCheck=true&enableBroadening=true"

# 发送GET请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
response = requests.get(url, headers=headers)

# 从响应内容中删除"jobsCallback("和最后的")"，然后解析JSON数据
data = json.loads(response.text[13:-1])

# 将数据写入本地JSON文件
with open("page.json", "w", encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
