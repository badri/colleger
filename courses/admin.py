from django.contrib import admin

from courses.models import Course, Unit, Lecture, Material, Vimeo, Enrolment

class CourseAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class UnitAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

class LectureAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Material)
admin.site.register(Vimeo)
admin.site.register(Enrolment)

