import wx
import wx.adv
import requests
import json
import re


class Frame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='2024_10_1_AQI_monitor', size=(680, 400))
        icon = wx.Icon(r'xiaomayisjh-head.png')
        self.SetIcon(icon)
        self.panel = wx.Panel(self)
        self.Center()
        self.init_ui()

    def init_ui(self):
        self.start_button = wx.Button(self.panel, size=(190, 80), pos=(30, 259), label='实时监测启动')
        start_button_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False,
                                    'Microsoft YaHei UI')
        self.start_button.SetFont(start_button_font)
        self.start_button.Bind(wx.EVT_BUTTON, self.on_start_button_click)

        image_path = r'github-blog-2dcode.png'
        image = wx.Image(image_path).Scale(200, 200).ConvertToBitmap()
        self.image_box = wx.StaticBitmap(self.panel, bitmap=image, size=(200, 200), pos=(24, 47))

        self.text = wx.StaticText(self.panel, size=(252, 27), pos=(-2, 11), label='2024_10_1_AQI_monitor')
        text_font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False,
                            'Microsoft YaHei UI')
        self.text.SetFont(text_font)

        self.output_box = wx.TextCtrl(self.panel, size=(360, 285), pos=(273, 12),
                                      style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.about_button = wx.adv.CommandLinkButton(self.panel, size=(129, 52), pos=(515, 304), mainLabel='关于',
                                                     note='xiaomayisjh')
        about_button_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False,
                                    'Microsoft YaHei UI')
        self.about_button.SetFont(about_button_font)
        self.about_button.Bind(wx.EVT_BUTTON, self.on_about_button_click)

    def on_start_button_click(self, event):
        self.output_box.Clear()
        public_ip = self.get_public_ip()
        latitude, longitude = self.get_location_by_ip(public_ip)
        formatted_latitude, formatted_longitude = self.format_coordinates(latitude, longitude)
        weather_data = self.get_weather_data(formatted_latitude, formatted_longitude)
        self.get_styled_air_quality_analysis(weather_data)

    def on_about_button_click(self, event):
        wx.MessageBox('这是一个空气质量监测工具。\n作者：xiaomayisjh', '关于', wx.OK | wx.ICON_INFORMATION)

    def get_public_ip(self):
        url = "https://api64.ipify.org?format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            ip_address = data['ip']
            return ip_address
        else:
            print("Error:", response.status_code)
            return None

    def get_location_by_ip(self, ip_address):
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

    def format_coordinates(self, latitude, longitude):
        formatted_latitude = round(latitude, 2)
        formatted_longitude = round(longitude, 2)
        return formatted_latitude, formatted_longitude

    def get_weather_data(self, latitude, longitude):
        weather_api_key = "API_KEY"
        api_url = f"https://devapi.qweather.com/v7/air/now?location={longitude},{latitude}&key={weather_api_key}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return {}

    def get_styled_air_quality_analysis(self, weather_data):
        url = "https://spark-api-open.xf-yun.com/v1/chat/completions"
        data = {
            "max_tokens": 4096,
            "top_k": 6,
            "temperature": 1,
            "messages": [
                {
                    "role": "user",
                    "content": f"请你扮演一个猫娘的风格，可爱地分析根据接下来的空气质量数据，不仅需要总体概括还需要分别分析每一种污染物的数据情况，每一小点分析可以卖个不同的萌，每次可爱的发言都要不同要有花样欧，可以在句末使用颜文字和表情符号，最后一句要撒个娇，不要提到我的风格要求：{weather_data}"
                }
            ],
            "model": "general",
            "stream": True
        }
        header = {
            "Authorization": "Bearer API_KEY:API_KEY"
        }
        response = requests.post(url, headers=header, json=data, stream=True)
        response.encoding = "utf-8"
        self.stream_response(response)

    def stream_response(self, response):
        for line in response.iter_lines(decode_unicode=True):
            if line:
                pattern = r'"content":"(.*?)"'
                matches = re.findall(pattern, line)
                content = ''.join(matches).replace('\\n', '\n')
                self.update_output(content)

    def update_output(self, content):
        wx.CallAfter(self.output_box.AppendText, content)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
