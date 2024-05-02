from django.db import models


# Create your models here.
class Game(models.Model):
	title = models.CharField(max_length=100)
	developer = models.CharField(max_length=100)
	release_date = models.DateField(blank=True)
	platform = models.CharField(max_length=50,  blank=True, null=True)
	genre = models.CharField(max_length=50,  blank=True)
	description = models.TextField(blank=True)
	cover = models.ImageField(upload_to='covers')

	def __str__(self):
		return self.title + ' by ' + self.developer
