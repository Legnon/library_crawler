from django.db import models


class Onepiece(models.Model):
	name = models.CharField(max_length=30)


class Denma(models.Model):
	name = models.CharField(max_length=30)
