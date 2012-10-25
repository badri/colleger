from django.conf.urls.defaults import *
'''
1.  add course/name/edit, course/name/analytics etc for course, unit and lecture.
2.  add view for instructors to manage students. This is only for course.
A graphical view with checkbox next to each student, paginated, along with student's progress in course.
ability to send bulk email to these students.
3. an ajax ui to upload material.
4. add video to a course/unit/lecture page
5. add quiz to a course/unit/lecture page
'''
urlpatterns = patterns('courses.views',
                       url(r'course/create/$', 'course_create'),
                       url(r'course/(?P<name>[\w\-]+)/$', 'course'),
                       url(r'course/(?P<name>[\w\-]+)/edit$', 'course_edit'),
                       url(r'course/(?P<name>[\w\-]+)/stats$', 'course_stats'),
                       # unit
                       url(r'course/(?P<name>[\w\-]+)/unit/add$', 'unit_create'),
                       url(r'unit/(?P<name>[\w\-]+)/$', 'unit'),
                       url(r'unit/(?P<name>[\w\-]+)/edit$', 'unit_edit'),
                       # lecture
                       url(r'lecture/create/$', 'lecture_create'),
                       url(r'lecture/(?P<name>[\w\-]+)/$', 'lecture'),
                       url(r'lecture/(?P<name>[\w\-]+)/edit$', 'lecture_edit'),
                       )
