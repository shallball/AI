本源码为python2.7环境下开发,利用神经网络模型实现对验证码的自动识别
1、yanzhengma.py 为生成验证码程序,在image文件夹中生成
2、gray.py 	 对image文件夹中的验证码图片进行灰度处理,并分割成四个字符分类存储在train文件夹下
3、cvsout.py     将train文件夹下的图片处理成train.csv数据文件
4、train.py	 将train.csv文件中的数据导入神经网络模型中进行训练,将训练结果存储在who.csv和wih.csv文件中
5、test.py	 导入who.csv和wih.csv文件中的数据,对test文件中的验证码进行结果测试
