from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.



class Circunscripcion(models.Model):
	nombre = models.CharField(max_length = 200, unique = True)
	nEscanos = models.IntegerField(default = 0)

	def __str__(self):
		return self.nombre

class Mesa(models.Model):
	nombre = models.CharField(max_length = 200, unique = True)
	circunscripcion = models.ForeignKey(Circunscripcion)

	def __str__(self):
		return self.nombre

class Partido(models.Model):
	nombre = models.CharField(max_length = 200, unique = True)

	def __str__(self):
		return self.nombre

class Resultado(models.Model):
	mesa = models.ForeignKey(Mesa)
	partido = models.ForeignKey(Partido)
	votos = models.IntegerField(default = 0)

	def __str__(self):
		return "El partido %s en la mesa %s tiene %d votos" % (self.partido, self.mesa, self.votos)

class UserProfile(models.Model):
	usuario = models.OneToOneField(settings.AUTH_USER_MODEL)

	def __unicode__(self):
		return self.usuario.username