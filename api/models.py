from django.db import models

# Create your models here.

class Sports(models.Model):
	name = models.CharField(max_length = 100)

	def __str__(self):
		return self.name

class Market(models.Model):
	name = models.CharField(max_length = 100)
	sports = models.ForeignKey(Sports, related_name = 'market', on_delete = models.CASCADE)

	def __str__(self):
		return self.name + ' | ' + self.sports.name

class Selection(models.Model):
	name = models.CharField(max_length = 100)
	odds = models.FloatField()
	market = models.ForeignKey(Market, related_name = 'selection', on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class Match(models.Model):
	name = models.CharField(max_length = 100)
	startTime = models.DateTimeField()
	sport = models.ForeignKey(Sports, related_name = 'match', on_delete = models.CASCADE)
	market = models.ForeignKey(Market, related_name = 'match', on_delete = models.CASCADE)

	class Meta:
		ordering = ('startTime',)
		verbose_name_plural = 'Matches'

	def __str__(self):
		return  self.name