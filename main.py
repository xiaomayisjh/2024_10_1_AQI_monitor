import requests
import json
import re


def get_location_by_ip(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        latitude = data.get('lat')
        longitude = data.get('lon')
        return latitude, longitude
    else:
        print("Error:", response.status_code)
        return None, None


def get_public_ip():
    url = "https://api64.ipify.org?format=json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        ip_address = data['ip']
        return ip_address
    else:
        print("Error:", response.status_code)
        return None


def format_coordinates(latitude, longitude):
    # 格式化经纬度坐标为最多小数点后两位
    formatted_latitude = round(latitude, 2)
    formatted_longitude = round(longitude, 2)
    return formatted_latitude, formatted_longitude


public_ip = get_public_ip()

# 示例IP地址
ip_address = public_ip
latitude, longitude = get_location_by_ip(ip_address)
print(f"Latitude: {latitude}, Longitude: {longitude}")
atted_latitude, formatted_longitude = format_coordinates(latitude, longitude)
print(f"atted_latitude: {atted_latitude}, formatted_longitude: {formatted_longitude}")

weather_api_key = f"df41819bc7c24afba7f5f7b25cb314a8"
api_url = f"https://devapi.qweather.com/v7/air/now?location={formatted_longitude},{atted_latitude}&key={weather_api_key}"

# 发送GET请求
response = requests.get(api_url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析返回的JSON数据
    air_quality_data = response.json()
    # print(air_quality_data)
else:
    print(f"Error: {response.status_code}")


# 展示数据
def display_data(data_dict, indent=0):
    for key, value in data_dict.items():
        if isinstance(value, dict):
            print("  " * indent + f"{key}:")
            display_data(value, indent + 1)
        elif isinstance(value, list):
            print("  " * indent + f"{key}:")
            for item in value:
                print("  " * (indent + 1) + f"- {item}")
        else:
            print("  " * indent + f"{key}: {value}")


# 调用函数展示所有数据
display_data(air_quality_data)

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
    "Authorization": "Bearer JNrMZQJoUoFRcKwGQAyv:RjGIChxVtsPwpwnoJgCG"
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
