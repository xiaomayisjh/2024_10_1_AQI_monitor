# -*- coding:utf-8 -*-
import wx.adv
import wx

class Frame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title='2024_10_1_AQI_monitor', size=(680, 400),name='frame',style=541072448)
		icon = wx.Icon(r'F:\HuaweiMoveData\Users\QFF\Desktop\xiaomayisjh\xiaomayisjh-head.png')
		self.SetIcon(icon)
		self.启动窗口 = wx.Panel(self)
		self.Centre()
		self.开始按钮 = wx.Button(self.启动窗口,size=(190, 80),pos=(30, 259),label='实时监测启动',name='开始')
		开始按钮_字体 = wx.Font(14,74,90,700,False,'Microsoft YaHei UI',28)
		self.开始按钮.SetFont(开始按钮_字体)
		self.开始按钮.Bind(wx.EVT_BUTTON,self.开始按钮_按钮被单击)
		图片框1_图片 = wx.Image(r'F:\HuaweiMoveData\Users\QFF\Desktop\xiaomayisjh\github-blog-2dcode.png').Scale(200, 200).ConvertToBitmap()
		self.图片框1 = wx.StaticBitmap(self.启动窗口, bitmap=图片框1_图片,size=(200, 200),pos=(24, 47),name='staticBitmap',style=0)
		self.文本 = wx.StaticText(self.启动窗口,size=(252, 27),pos=(-2, 11),label='2024_10_1_AQI_monitor',name='staticText',style=2321)
		文本_字体 = wx.Font(15,74,90,700,False,'Microsoft YaHei UI',28)
		self.文本.SetFont(文本_字体)
		self.输出框 = wx.TextCtrl(self.启动窗口,size=(360, 285),pos=(273, 12),value='',name='输出',style=1073741872)
		self.关于 = wx.adv.CommandLinkButton(self.启动窗口,size=(129, 52),pos=(515, 304),name='关于',mainLabel='关于',note='xiaomayisjh')
		关于_字体 = wx.Font(11,74,90,400,False,'Microsoft YaHei UI',28)
		self.关于.SetFont(关于_字体)
		self.关于.Bind(wx.EVT_BUTTON,self.关于_按钮被单击)


	def 开始按钮_按钮被单击(self,event):
		print('开始按钮,按钮被单击')


	def 关于_按钮被单击(self,event):
		print('关于,按钮被单击')

class myApp(wx.App):
	def  OnInit(self):
		self.frame = Frame()
		self.frame.Show(True)
		return True

if __name__ == '__main__':
	app = myApp()
	app.MainLoop()