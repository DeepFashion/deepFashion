from threading import Lock
clientLock=Lock()
class caffeThreadManager:
	def __init__(self,numThreads):
		self.threadPool = []
		self.createPool(numThreads)

	def _create_caffe_client(self):
		pass
		# try:
		# 	c = client.Client(self.clientIP, self.clientPort)
		# 	return c
		# except:
		# 	print 'Connection to Client Failed, Check if the weaver instance is running'
		# 	return None

	def createPool(self,numThreads):
		with clientLock:
			for i in range(numThreads):
				c = self._create_caffe_client()
				if c:
					self.threadPool.append(c)
				else:
					return False

	def getThread(self):
		with clientLock:
			if self.threadPool:
				c = self.threadPool[-1]
				self.threadPool.pop()
				return c
			else:
				return self._create_caffe_client()

	def returnThread(self,c):
		with clientLock:
			self.threadPool.append(c)