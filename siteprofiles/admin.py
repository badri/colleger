from django.contrib import admin
from siteprofiles.models import Student, Employer
from models import User

admin.site.unregister(User)
admin.site.register(Student)
admin.site.register(Employer)
