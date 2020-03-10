#coding=utf-8
import os,csv
from PIL import Image
import numpy as np
import scipy.misc
dirs=os.listdir("./train")
out=open("train.csv","wb")
for i in dirs:
	t=0
	for j in os.listdir("./train/%s"%i):
		t+=1
		if t>200:
			break
		if i.isdigit():
			num=int(i)
		else:
			if i[1]=="0":
				num=(ord(i[0])-97)*2+10
			if i[1]=="1":
				num=(ord(i[0])-97)*2+11
		c=[]
		c.append(num)

		img=Image.open("./train/%s/%s"%(i,j))
		img=img.resize((28,28),Image.ANTIALIAS)
		#b=Image.fromarray(img_array).convert("RGB")
		#img.show()
		img=np.array(img.convert("L"),"f",)
		img=255-img
		for m in img:
			for n in m:					
				c.append(float(n))
		csv_write=csv.writer(out)
		csv_write.writerow(c)

