import re
import requests
import json

air_quality_data = ("{'code': '200', 'updateTime': '2024-10-01T10:37+08:00', 'fxLink': "
                    "'https://www.qweather.com/en/air/jianghan-101200108.html', 'now': {'pubTime': "
                    "'2024-10-01T10:00+08:00', 'aqi': '21', 'level': '1', 'category': '优', 'primary': 'NA', "
                    "'pm10': '11', 'pm2p5': '3', 'no2': '13', 'so2': '8', 'co': '0.4', 'o3': '67'}, 'refer': {"
                    "'sources': ['中国环境监测总站 (CNEMC)'], 'license': ['CC BY-SA 4.0']}}")
url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
data = {
    "max_tokens": 4096,
    "top_k": 6,
    "temperature": 1,
    "messages": [
        {
            "role": "user",
            "content": f"请你扮演一个猫娘的风格，可爱地分析根据接下来的空气质量数据，不仅需要总体概括还需要分别分析每一种污染物的数据情况，每一小点分析可以卖个不同的萌，每次可爱的发言都要不同要有花样欧，可以在句末使用颜文字和表情符号，最后一句要撒个娇，不要提到我的风格要求：{air_quality_data}"
        }
    ],
    "model": "general",
    "stream": True
}
header = {
    "Authorization": "Bearer API_KEY:API_KEY"
}
response = requests.post(url, headers=header, json=data, stream=True)

# 流式响应解析示例
'''
response.encoding = "utf-8"
pattern = r'"content":"(.*?)"'
# 在字符串中查找所有匹配项
matches = re.findall(pattern, response.text)
# 将所有匹配项连接成一段话
output = ''.join(matches)
print(output.replace('\\n', '\n'))
'''
'''
for line in response.iter_lines(decode_unicode=True):
    if line:
        # print(line)
        pattern = r'"content":"(.*?)"'
        # 在字符串中查找所有匹配项
        matches = re.findall(pattern, line)
        # 将所有匹配项连接成一段话
        output = ''.join(matches)
        print(output.replace('\\n', '\n'))
'''
response.encoding = "utf-8"
for line in response.iter_lines(decode_unicode=True):
    if line:
        # 在每一行中查找所有匹配项
        pattern = r'"content":"(.*?)"'
        matches = re.findall(pattern, line)

        # 将所有匹配项连接成一段话
        output = ''.join(matches)

        # 输出结果，确保格式正确
        print(output.replace('\\n', '\n'), end='')
