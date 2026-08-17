from django.db import models
from datetime import date

# Create your models here.
class Robot(models.Model) :
	robot_id = models.CharField(max_length=20, primary_key=True)
	pos_x = models.IntegerField()
	pos_y = models.IntegerField()
	battery = models.IntegerField()
	joined_at = models.DateField(default=date.today)

	def __str__(self) :
		return f'Robot : {self.robot_id}, \
				Current cordinate : {self.pos_x}, {self.pos_y}'

