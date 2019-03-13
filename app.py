import win32gui as wg
import pyautogui as pg
from PIL import ImageGrab
from PIL import Image
import cv2
import numpy as np
import time
import mouse
import os
import re
import datetime

from SolveCaphcha import SolveCaphca

#Window NoxPlayer
hwnd = wg.FindWindowEx(0,0,None, 'NoxPlayer')

#Templates path
path = 'buttons/'

#Windows
windows = ['profile','sv_captcha','google_capcha','profit','reklama']
windows_templates = []
for window in windows:
	windows_templates.append(cv2.imread(path + str(window) +'.png',0))

#Profit butons
btns = []
for i in range(1,5):
	btns.append(cv2.imread(path + str(i) +'.png',0))


back_btn = cv2.imread(path + 'back.png',0)
cancel_btn = cv2.imread(path + 'cancel.png',0)

#Super Vank Captcha
#sv_captcha = cv2.imread(path + 'sv_capcha.png',0)

#Closing Reklam

#window coor
left, top, right, bot = wg.GetWindowRect(hwnd)
w = right - left
h = bot - top
###capcha table

tb_left		= int(left+(w*(7.0/100)))
tb_right	= int(right-(w*(7.0/100)))
tb_top		= int(top+(h*(40/100)))
tb_bot		= int(bot-(h*(32.3/100)))

table_width	= tb_right - tb_left
row_width	= table_width/6
row_Hcenter	= tb_left + row_width/2

table_height= tb_bot - tb_top
row_height	= table_height/6
row_Vcenter = tb_top + row_height/2

def row_coords():
	tab_nums = []
	for y in range(0,6):
		for x in range(0,6):
			tab_nums.append([row_Hcenter + row_width*x, row_Vcenter + row_height*y])
	return tab_nums


def scrape_screen():
	im = ImageGrab.grab(bbox=(left,top,right,bot))
	im = im.convert('RGB')
	return np.array(im)

def mouse_click_btn(gg):
	pg.moveTo(left+gg[0],top+gg[1])
	mouse.click(button = 'left')

def mouse_click(x,y):
	pg.moveTo(x,y)
	mouse.click(button = 'left')

def mouse_click_row(gg):
	pg.moveTo(gg[0], gg[1])
	mouse.click(button = 'left')

def getReferenceCoords(screen, templates):
		# output = ''
		img_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

		# for idx, template in enumerate(card_templates):
		res = cv2.matchTemplate(img_gray, templates,cv2.TM_CCOEFF_NORMED)
		loc = np.where( res >= 0.90)

		for pt in zip(*loc[::-1]):
			return pt
		return False
		pass

def scrape_profit_btn():
	for btn in btns:
		scrape_btns = getReferenceCoords(scrape_screen(), btn)
		if scrape_btns!=False:
			mouse_click_btn(scrape_btns)
			break


count = 0
while True:
	ss = scrape_screen()
	profile = getReferenceCoords(ss, windows_templates[0])
	sv_cap = getReferenceCoords(ss, windows_templates[1])
	gl_cap = getReferenceCoords(ss, windows_templates[2])
	profit = getReferenceCoords(ss, windows_templates[3])
	reklama = getReferenceCoords(ss, windows_templates[4])

	if profile!=False and profit==False and sv_cap==False and gl_cap==False:
		count = 0
		scrape_profit_btn()
		print('Click to view ads')
	elif sv_cap:
		count = 0
		print('Solving Captcha')
		h_, w_ = windows_templates[1].shape
		x = left + sv_cap[0]
		y = top + sv_cap[1]
		solve_capcha = SolveCaphca(x,y,w_,h_)
		nums = solve_capcha.get_capcha()
		table = row_coords()
		if nums != []:
			for num in nums:			
				mouse_click_row(table[int(num)-1])
		else:
			cancel = getReferenceCoords(ss, cancel_btn)
			mouse_click_btn(cancel)

	elif gl_cap:
		#mouse_click_btn(gl_cap)
		print('ReCaptcha')
	
	elif profit:
		count = 0
		mouse_click_btn(profit)
		print('profit')
	
	elif reklama:
		count +=1
		print('reklama')
		print(count)
		if count > 15:
			mouse_click(right+20,bot-100)
		
	else:
		count = 0
		print('Wait!!!')
	time.sleep(2)




# sb = getReferenceCoords(open_cv_image, sv_captcha)
# if sb!=False:
# 	print('Super Vank Captcha Solving')
# if





