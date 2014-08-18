from django.contrib import admin
from documents.models import Document,File,Payment
# Register your models here.
admin.site.register(Document)
admin.site.register(File)
admin.site.register(Payment)
