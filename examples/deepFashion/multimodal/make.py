def make(f1,f2):
	wf=open(f2,'w+')
	data=list()
	with open(f1,'r') as f:
		data=f.readlines()
	for line in data:
		line=line.strip()
		line=line.split(" ")
		val=line[0]+" "+line[1]
		wf.write(val+'\n')
	wf.close()

make('train.txt','train_1.txt')
make('test.txt','test_1.txt')

