import redis
import json
r_server = redis.Redis('localhost') #this line creates a new Redis object and
                                    #connects to our redis server
def insertKey(key,value):
	value=json.dumps(value)
	r_server.set(key, value)


def fetchKey(key):
	try:
		return json.loads(r_server.get(key))
	except:
		return None