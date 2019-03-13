import cv2
from PIL import ImageGrab
import os
import re

class SolveCaphca:
	#coor - template coords
	def __init__(self,x,y,w,h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def get_capcha_screen(self):
		print(self.x, self.y)
		print(self.w, self.h)
		# im = ImageGrab.grab(bbox=(self.x+self.w,
		# 						self.y, self.x+self.w+65,self.y+self.h))
		# im = im.convert('RGB')
		box=(self.x+self.w,self.y, self.x+self.w+60,self.y+self.h)
		ImageGrab.grab().crop(box).save("scr_cap/screen_capture.png", "PNG")

	
	def get_capcha(self):
		self.get_capcha_screen()
		os.system("tesseract scr_cap/screen_capture.png text")
		solve_file = open('text.txt','r')
		solve = re.findall('\d+',solve_file.read())
		print(solve)
		if(os.path.exists('scr_cap/screen_capture.png') or (os.path.exists(solve[0]+'_'+solve[1]+'.png'))):
			try:
				os.rename('scr_cap/screen_capture.png', solve[0]+'_'+solve[1]+'.png')
			except:
				pass
		return solve
		
