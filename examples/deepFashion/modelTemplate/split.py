with open(PROJECT+'/SETTINGS.json', 'r') as content_file:
	settings = json.load(content_file)
FILENAME_TRAIN = settings['TEST_FILE']
FILENAME_TEST = settings['TRAIN_FILE']

def main(FILENAME):
	with open(FILENAME,'r') as f:
		data=f.readlines()
	str1=""
	str2=""
	for i in range(len(data)):
		str1+=data[i].split(' ')[0].strip()+'\n'
		str2+=data[i].split(' ')[1].strip()+'\n'
	with open(FILENAME+'.data','w+') as f:
		f.write(str1)
	with open(FILENAME+'.labels','w+') as f:
		f.write(str2)
main(FILENAME_TRAIN)
main(FILENAME_TEST)