from django.contrib import admin
from .models import Pipeline,ActiveBB, BB, editor

# Register your models here.
admin.site.register(Pipeline)
admin.site.register(ActiveBB)
admin.site.register(BB)
admin.site.register(editor)