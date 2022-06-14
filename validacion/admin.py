from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html

from validacion.models import Valido, Integridad, Firma, Llave
from validacion.CA_code import crear_clave, crear_csr, firma_cert

import os
import hashlib

# Register your models here.

@admin.register(Valido)
class VerificarAdmin(admin.ModelAdmin):
    pass

@admin.register(Integridad)
class IntegridadAdmin(admin.ModelAdmin):
    list_display = ['frase', 'get_doc', 'hash']

    def save_model(self, request, obj, form, change):
        '''
        m = hashlib.sha256()
        m.update(request.FILES['documento'].read())
        m.update(str.encode(request.POST.get('frase')))

        print(m.digest())
        '''

        super().save_model(request, obj, form, change)

    def hash(self, obj):
        path = os.path.join(settings.BASE_DIR, str(obj.documento))
        m = hashlib.sha256()
        with open(path, 'rb') as f:
            m.update(f.read())

        return m.hexdigest()

    def get_doc(self, obj):
        return obj.documento

    get_doc.short_description = 'Documento'

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def has_change_permission(self, request, obj = None):
        return False

@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'pais', 'estado', 'ciudad', 'organizacion', 'departamento', 'correo','get_cert']

    def save_model(self, request, obj, form, change):
        nombre = request.POST.get('nombre')
        pais = request.POST.get('pais')
        estado = request.POST.get('estado')
        ciudad = request.POST.get('ciudad')
        organizacion = request.POST.get('organizacion')
        departamento = request.POST.get('departamento')
        correo = request.POST.get('correo')
        contrasena=request.POST.get('contrasena')
        crear_clave(nombre,contrasena)
        path_csr = crear_csr(nombre, pais, estado, ciudad, organizacion, departamento, correo,contrasena)
        firma_cert(path_csr, nombre)

        super().save_model(request, obj, form, change)

    def get_cert(self, obj):
        #path = os.path.join(settings.BASE_DIR, 'raiz/CA/intermedio/certs/', '{}.cert.pem'.format(obj.nombre))
        path = os.path.join('media/', '{}.cert.pem'.format(obj.nombre))
        cert = '{}.cert.pem'.format(obj.nombre)

        #path = 'file:///' + path
        path = os.path.join('http://localhost:8000', path)

        return format_html("<a href='{}'>{}</a>".format(path, cert))

    get_cert.short_description = 'Certificado'

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save_and_add_another': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

    def has_change_permission(self, request, obj = None):
        return False

@admin.register(Llave)
class LlavesAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Firma, FirmaAdmin)
