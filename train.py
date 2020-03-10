#coding=utf-8
import numpy,csv,random
import scipy.special


class neuralNetwork:
	def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
		self.inodes=inputnodes
		self.hnodes=hiddennodes
		self.onodes=outputnodes
		self.wih=numpy.random.normal(0.0,pow(self.hnodes,-0.5),
		(self.hnodes,self.inodes))
		self.who=numpy.random.normal(0.0,pow(self.onodes,-0.5),
		(self.onodes,self.hnodes))
		self.lr=learningrate
		self.activation_function=lambda x:scipy.special.expit(x)
		pass
	
	def train(self,inputs_list,targets_list):
		inputs=numpy.array(inputs_list,ndmin=2).T
		targets=numpy.array(targets_list,ndmin=2).T
		hidden_inputs=numpy.dot(self.wih,inputs)
		hidden_outputs=self.activation_function(hidden_inputs)
		final_inputs=numpy.dot(self.who,hidden_outputs)
		final_outputs=self.activation_function(final_inputs)
		output_errors=targets-final_outputs
		hidden_errors=numpy.dot(self.who.T,output_errors)
		self.who+=self.lr*numpy.dot((output_errors*final_outputs*
		(1-final_outputs)),numpy.transpose(hidden_outputs))
		self.wih+=self.lr*numpy.dot((hidden_errors*hidden_outputs*
		(1-hidden_outputs)),numpy.transpose(inputs))
		pass
		
	def query(self,inputs_list):
		inputs=numpy.array(inputs_list,ndmin=2).T
		hidden_inputs=numpy.dot(self.wih,inputs)
		hidden_outputs=self.activation_function(hidden_inputs)
		final_inputs=numpy.dot(self.who,hidden_outputs)
		final_outputs=self.activation_function(final_inputs)
		
		return final_outputs

input_nodes=784
hidden_nodes=300
output_nodes=62
learning_rate=0.1

	
n=neuralNetwork(input_nodes,hidden_nodes,output_nodes,learning_rate)
training_data_file=open("train.csv",'r')
training_data_list=training_data_file.readlines()
random.shuffle(training_data_list)
training_data_file.close()
print len(training_data_list)


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
	
n.who=numpy.array(who)
n.wih=numpy.array(wih)

epochs=200
for e in range(epochs):
	print u"训练次数:%s"%e
	for record in training_data_list:		
		all_values=record.split(',')		
		inputs=(numpy.asfarray(all_values[1:])/255.0*0.99)+0.01
		targets=numpy.zeros(output_nodes)+0.01
		targets[int(all_values[0])]=0.99		
		n.train(inputs,targets)

training_data_file.close()
out=open("who.csv","wb")
csv_write=csv.writer(out)
csv_write.writerows(n.who)
out=open("wih.csv","wb")
csv_write=csv.writer(out)
csv_write.writerows(n.wih)

