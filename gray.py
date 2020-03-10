#coding=utf-8
from PIL import Image
import numpy as np
import time,os
#创建文件夹
try:
	for i in range(26):
		os.makedirs("./train/%s0"%chr(97+i))
		os.makedirs("./train/%s1"%chr(97+i))
	for i in range(10):	
		os.makedirs("./train/%s"%i)
except:
	pass
#将验证码拆分成四个字符并分类保存	
for dirpath, dirnames, filenames in os.walk("./image"):

	for t in range(len(filenames)):
		
		img=np.array(Image.open("./image/%s"%filenames[t]).convert("L"),"f")

		im0=[]
		im1=[]
		im2=[]
		im3=[]
		im4=[]
		#找出不是白色的点
		for i in range(160):
			for j in range(70):
				if img[j][i]<250:
					im0.append([j,i])
		#将四个字符的图片分开
		names=locals()		
		try:
			for n in range(4):
				while 1:
					names["im"+str(n+1)].append(im0[0])
					while 1:
						new=0
						for i in im0:
							for j in names["im"+str(n+1)]:
								if -1<=j[0]-i[0]<=1 and -1<=j[1]-i[1]<=1:
									new=1

									names["im"+str(n+1)].append(i)
									im0.remove(i)
									break
							if new==1:
								break		
						
						if new==0:
							break	
					names["ave_x"+str(n+1)]=0
					if len(names["im"+str(n+1)])>40:		#输出像素点数量多于40的图
						names["img"+str(n+1)]=[([255]*200) for i in range(70)]	#创建200*70像素扩宽
						for i in names["im"+str(n+1)]:
							names["ave_x"+str(n+1)]+=i[1]
							names["img"+str(n+1)][i[0]][i[1]+20]=img[i[0]][i[1]]
						names["ave_x"+str(n+1)]=names["ave_x"+str(n+1)]/len(names["im"+str(n+1)])+20
						a=np.array(names["img"+str(n+1)])
						a=a[:,(names["ave_x"+str(n+1)]-25):(names["ave_x"+str(n+1)]+25)]
						names["img"+str(n+1)]=Image.fromarray(a)
						#判断大小写
						
						if filenames[t][n].islower():
							filename=filenames[t][n]+"0"
						elif filenames[t][n].isupper():
							filename=filenames[t][n]+"1"
						else:
							filename=filenames[t][n]			
						names["img"+str(n+1)].convert("RGB").save("./train/%s/%s.png"%(filename,(t*4+n)))
						break
		except:
			print u"验证码"+filenames[t]+u" 分割错误"
	
		

