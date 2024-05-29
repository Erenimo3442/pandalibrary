from django.db import models


# Create your models here.
class Game(models.Model):
	STATUS_CHOICES = [
		('PC', 'PC'),
		('Playstation', 'Playstation'),
		('Xbox', 'Xbox'),
		('Mobile', 'Mobile'),
	]
	title = models.CharField(max_length=100)
	developer = models.CharField(max_length=100)
	release_date = models.DateField(null=True, blank=True)
	platform = models.CharField(max_length=50, choices=STATUS_CHOICES, blank=True, null=True)
	genre = models.CharField(max_length=50,  blank=True)
	description = models.TextField(blank=True)
	cover = models.ImageField(upload_to='covers', blank=True, null=True)
	average_rating = models.FloatField(default=0)

	def __str__(self):
		return self.title + ' by ' + self.developer
