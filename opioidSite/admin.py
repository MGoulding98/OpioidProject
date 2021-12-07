from django.contrib import admin
from .models import Drug, Prescriber, Statedata, Triple
# Register your models here.
admin.site.register(Drug)
admin.site.register(Prescriber)
admin.site.register(Statedata)
admin.site.register(Triple)