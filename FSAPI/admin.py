from django.contrib import admin
from .models import Topic
from .models import Folder
from .models import Document

admin.site.register(Topic)
admin.site.register(Folder)
admin.site.register(Document)
