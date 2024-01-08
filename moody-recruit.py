import requests
from bs4 import BeautifulSoup
import pandas as pd

# 请求 Moody's 职业机会网页
# url = "https://careers.moodys.com/job-search-results/"
url = "https://jobsapi-google.m-cloud.io/api/job/search?callback=jobsCallback&pageSize=1000&offset=0&companyName=companies%2Fd475e46c-52e0-4b9b-a525-48027b002583&customAttributeFilter=ats_portalid%3D%22SuccessFactors%22&orderBy=posting_publish_time%20desc&disableSpellCheck=true&enableBroadening=true"
response = requests.get(url)
# print the response text (the content of the requested file):
# 分行打印 response 中所有含有'job'的内容
for line in response:
    if "job_title".encode() in line:
        print(line)

    # print(response.text)
# 解析网页内容
soup = BeautifulSoup(response.text, 'html.parser')

# 查找所有职位列表项
jobs = soup.find_all('div', class_='jobTitle')
# soap.find_all的语法
# find_all(name, attrs, recursive, string, limit, **kwargs)
# name: 对标签名称的检索字符串
# attrs: 对标签属性值的检索字符串，可标注属性检索
# recursive: 是否对子孙全部检索，默认True
# string: <>...</>中字符串区域的检索字符串
# limit: 对返回结果数量的限制
# **kwargs: 用于属性检索的参数，如id=’head’


# 提取职位信息
data = []
for job in jobs:
    title = job.find('h3', class_='jobTitle').text
    location = job.find('span', class_='job-location').text
    date = job.find('span', class_='job-date-posted').text

    # 获取职位详细页面的链接
    link = job.find('a')['href']

    # 请求职位详细页面
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取职位要求
    requirements = soup.find('div', class_='job-requirements').text

    data.append([title, location, date, requirements])

# 创建 DataFrame 并保存为 CSV 文件
df = pd.DataFrame(data, columns=['Title', 'Location', 'Date', 'Requirements'])
df.to_csv('moodys_jobs.csv', index=False)
