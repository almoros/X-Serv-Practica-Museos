from django.contrib import admin
from .models import Museo, Usuario, Fecha, Comentario

# Register your models here.
admin.site.register(Museo)
admin.site.register(Usuario)
admin.site.register(Fecha)
admin.site.register(Comentario)
