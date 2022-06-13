from django.db import models

# Create your models here.
#class Certificado(models.Model):

class Valido(models.Model):
    firma = models.TextField()
    documento = models.FileField(upload_to = 'documentos/')
    certificado = models.FileField(upload_to = 'certificados/')

class Persona(models.Model):
    nombre = models.TextField()
    apellido = models.TextField()

class Firma(models.Model):
    documento = models.FileField(upload_to = 'documentos/')
    privada = models.TextField()
    password = models.TextField()
    certificado = models.FileField(upload_to = 'certificados/')

class Llave(models.Model):
    publica = models.TextField()
    privada = models.TextField()
    password = models.TextField()
    persona = models.ForeignKey(Persona, on_delete = models.CASCADE)
