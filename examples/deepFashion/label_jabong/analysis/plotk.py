import matplotlib.pyplot as plt
with open ('precision-at-k.txt','r') as f:
	data=f.readlines()
arr1=list()
arr2=list()
for line in data:
	line=line.strip()
	line=line.split('   ')
	arr1.append(line[0])
	arr2.append(line[1])

plt.plot(arr1, arr2)
plt.xlabel('k')
plt.ylabel('Precision')
plt.title('{Precison at k')
plt.show()