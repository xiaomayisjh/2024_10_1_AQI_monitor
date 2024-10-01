import requests
import json
import re
import json

# 示例输入数据
data = '''
{
    "code": "200",
    "updateTime": "2024-10-01T10:37+08:00",
    "fxLink": "https://www.qweather.com/en/air/jianghan-101200108.html",
    "now": {
        "pubTime": "2024-10-01T10:00+08:00",
        "aqi": "21",
        "level": "1",
        "category": "优",
        "primary": "NA",
        "pm10": "11",
        "pm2p5": "3",
        "no2": "13",
        "so2": "8",
        "co": "0.4",
        "o3": "67"
    },
    "refer": {
        "sources": ["中国环境监测总站 (CNEMC)"],
        "license": ["CC BY-SA 4.0"]
    }
}
'''

# 解析JSON数据
parsed_data = json.loads(data)

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
display_data(parsed_data)
