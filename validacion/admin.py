from django.contrib import admin

from validacion.models import Valido, Persona, Firma, Llave

# Register your models here.

@admin.register(Valido)
class VerificarAdmin(admin.ModelAdmin):
    pass

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    pass

@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    pass

@admin.register(Llave)
class LlavesAdmin(admin.ModelAdmin):
    pass
