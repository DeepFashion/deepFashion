import optparse
import os
def parse_args():

	usage="""
		use flag --name with arguement to specify project name 
		use flag --root to specify the root folder(empty for default)
		use flag --local to specify the local root folder(empty for default)
		use flag --db to specify the directory for the database

	"""
	parser = optparse.OptionParser(usage)

	help = "Name of the Project, default None"
	parser.add_option('--name', default=None,help=help)

	help = "root folder for the project, default /home/ubuntu/caffe-cvprw15/examples/deepFashion"
	parser.add_option('--root', help=help, default='/home/ubuntu/caffe-cvprw15/examples/deepFashion')

	help = "local folder for the project, default /home/siddhantmanocha/Projects/...."
	parser.add_option('--local', help=help, default='/home/siddhantmanocha/Projects/neural/deepFashion/examples/deepFashion')

	help = "db folder for the project, default /data/deepfashion"
	parser.add_option('--db', help=help, default='/data/deepfashion')

	options, args = parser.parse_args()

	if options.root[-1]=='/':
		options.root=options.root[:-1]

	if options.local[-1]=='/':
		options.local=options.local[:-1]

	if options.db[-1]=='/':
		options.db=options.db[:-1]

	if (os.path.isdir(options.root)):
		pass
	else:
		parser.error('Project Root Directory Does Not Exist')

	if not options.name:
	    parser.error('Name is required')

	return options

if __name__ == '__main__':
	options=parse_args()
	print options
			

