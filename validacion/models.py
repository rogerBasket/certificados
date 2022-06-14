from django.db import models

# Create your models here.
#class Certificado(models.Model):

class Valido(models.Model):
    firma = models.TextField()
    documento = models.FileField(upload_to = 'documentos/')
    certificado = models.FileField(upload_to = 'certificados/')

class Integridad(models.Model):
    frase = models.TextField()
    documento = models.FileField()

class Firma(models.Model):
    nombre = models.TextField()
    pais = models.TextField()
    estado = models.TextField(default = '')
    ciudad = models.TextField(default = '')
    organizacion = models.TextField(default = '')
    departamento = models.TextField(default = '')
    correo = models.TextField(default = '')
    contrasena = models.TextField(default = '')

class Llave(models.Model):
    publica = models.TextField()
    privada = models.TextField()
    password = models.TextField()
    #persona = models.ForeignKey(Persona, on_delete = models.CASCADE)
