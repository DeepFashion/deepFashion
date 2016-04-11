from threading import Lock
import predictTags as predict
class caffeThreadManager:
	def __init__(self,numThreads,settings_file):
		self.threadPool = []
		self.settings_file=settings_file
		self.createPool(numThreads)
		self.clientLock=Lock()

	def _create_caffe_client(self):
		try:
			c = predict.CreateClassifier(self.settings_file)
			print "Creating caffe client"
			return c
		except:
			print 'Some error'
			return None

	def createPool(self,numThreads):
		with self.clientLock:
			for i in range(numThreads):
				c = self._create_caffe_client()
				if c:
					self.threadPool.append(c)
				else:
					return False

	def getThread(self):
		with self.clientLock:
			if self.threadPool:
				c = self.threadPool[-1]
				self.threadPool.pop()
				return c
			else:
				return self._create_caffe_client()

	def returnThread(self,c):
		with self.clientLock:
			self.threadPool.append(c)