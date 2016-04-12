from django.db import models
from djangotoolbox.fields import ListField,DictField
from datetime import datetime
from django.db.models.signals import post_save
import json
class products(models.Model):
	imageName=models.TextField()  
	similarProducts = models.TextField() 
	tags=models.TextField() 
	crossProducts =models.TextField()  

	def to_json(self):
		return {
				"_id":self.id,
				"imageName":self.imageName,
				"similarProducts" : json.loads(self.similarProducts),
				"tags": json.loads(self.tags),
				"crossProducts": json.loads(self.crossProducts)
			}

	class Meta:
		db_table = 'products'





