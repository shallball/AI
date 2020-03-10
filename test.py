#coding=utf-8
import csv,os,time
import numpy as np
import scipy.special
from PIL import Image
training_data_file=open("who.csv",'r')
a=training_data_file.readlines()
training_data_file.close()

training_data_file=open("wih.csv",'r')
b=training_data_file.readlines()
training_data_file.close()

who=[]
wih=[]
for record in a:
	who.append(map(lambda x:float(x),record.split(",")))
for record in b:
	wih.append(map(lambda x:float(x),record.split(",")))
		
class neuralNetwork:
	def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
		self.inodes=inputnodes
		self.hnodes=hiddennodes
		self.onodes=outputnodes
		self.wih=np.random.normal(0.0,pow(self.hnodes,-0.5),
		(self.hnodes,self.inodes))
		self.who=np.random.normal(0.0,pow(self.onodes,-0.5),
		(self.onodes,self.hnodes))
		self.lr=learningrate
		self.activation_function=lambda x:scipy.special.expit(x)
		pass
	def query(self,inputs_list):
		inputs=np.array(inputs_list,ndmin=2).T
		hidden_inputs=np.dot(self.wih,inputs)
		hidden_outputs=self.activation_function(hidden_inputs)
		final_inputs=np.dot(self.who,hidden_outputs)
		final_outputs=self.activation_function(final_inputs)
		
		return final_outputs	

input_nodes=784
hidden_nodes=300
output_nodes=62
learning_rate=0.1
ne=neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)


ne.who=who
ne.wih=wih

for dirpath, dirnames, filenames in os.walk("./test"):

	for t in range(len(filenames)):
		img=np.array(Image.open("./test/%s"%filenames[t]).convert("L"),"f")

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
		names=globals()
		
		result=""
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
					if len(names["im"+str(n+1)])>60:		#输出像素点数量多于60的图
						names["img"+str(n+1)]=[([255]*200) for i in range(70)]	#创建200*70像素扩宽
						for i in names["im"+str(n+1)]:
							names["ave_x"+str(n+1)]+=i[1]
							names["img"+str(n+1)][i[0]][i[1]+20]=img[i[0]][i[1]]
						names["ave_x"+str(n+1)]=names["ave_x"+str(n+1)]/len(names["im"+str(n+1)])+20
						a=np.array(names["img"+str(n+1)])
						a=a[:,(names["ave_x"+str(n+1)]-25):(names["ave_x"+str(n+1)]+25)]
						a=Image.fromarray(a)
						a=a.resize((28,28),Image.ANTIALIAS)
						#a.show()
						a=np.array(a.convert("L"),"f",)
						a=255-a
						'''b=Image.fromarray(a).convert("RGB")
						b.show()'''
						
						inp=[]
						for m0 in a:
							for n0 in m0:					
								inp.append(n0)
						
						try:		
							inputs=(np.asfarray(inp[:])/255.0*0.99)+0.01
							
							outputs=ne.query(inputs)

							label=np.argmax(outputs)
							
							if label<10:
								label==label
							else:
								if label%2==0:
									label=chr((label-10)/2+97)
								else:
									label=chr((label-11)/2+65)
							
							result=result+"%s"%label	
						except:
							pass
						break
			print u"识别结果:"+result	
		except:
			pass	
						
						
									
			
