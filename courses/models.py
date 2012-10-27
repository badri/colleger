from quiz.models import Quiz

from taggit.managers import TaggableManager
from polymorphic import PolymorphicModel

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from courses.fields import PercentField

'''
TODO:
1. merge quiz and category with this app. - category will be converted to django tagging app.
2. add oembed capability for major providers like vimeo. - not needed
3. send bulk email to course members about new unit notifications, quiz, exam, last date, results etc.
4. course level stats, like 
  a. no. of enrollments per day  - new model, maybe merged with CourseProgress
  b. % pass, % completion
  c. demographics, like which discipline students, which college enrolls most
5. forum integration using Askbot - skipped for MVP
6. course/unit/lecture locking, where one unit depends on another course/unit/lecture to be finished. - done
7. still no sense of a student finishing a course, when has a student finished a course?  - new model called CourseProgress
8. oembed and video integration - skipped, instead, django attachments will be used.
9. lecture, unit dates must validate within course dates, if specified.
10. How to ban a student from a course? show a view that student is banned and has to contact site admin etc when he views a course.
11. all course pages must only be available on signin, or enroll button takes you to signin page(you signin as a student).
12. Never allow assignment submission past deadline....
13. add News model for each course. - skipped for MVP
'''

class Session(PolymorphicModel):
    title = models.CharField(_('title'), max_length=150)

class Course(Session):
    slug = models.SlugField(_('slug'))
    tags = TaggableManager()
    description = models.TextField(_('description'), blank=True, null=True)
    start_date = models.DateField(_('course start date'), auto_now_add=True)
    end_date = models.DateField(_('course end date'), blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    syllabus = models.TextField(_('course syllabus'), blank=True, null=True)
    software = models.TextField(_('required software/materials'), blank=True, null=True)
    references = models.TextField(_('Recommended Reference Books'), blank=True, null=True)
    faculty = models.ManyToManyField(User, related_name='faculty')
    dependent_courses = models.ManyToManyField(Session, null=True, blank=True, related_name='depends_on')

    def __unicode__(self):
        return u'%s' % self.title

    def get_units(self):
        return Unit.objects.filter(course=self)

class Unit(Session):
    slug = models.SlugField(_('slug'))
    course = models.ForeignKey(Course)
    description = models.TextField(_('description'), blank=True, null=True)
    start_date = models.DateField(_('unit start date'), auto_now_add=True)
    end_date = models.DateField(_('unit end date'), blank=True, null=True)

    def get_lectures(self):
        return Lecture.objects.filter(unit=self)

class Lecture(Session):
    slug = models.SlugField(_('slug'))
    unit = models.ForeignKey(Unit)
    lecture_date = models.DateField(_('When was the lecture held'))
    description = models.TextField(_('description'), blank=True, null=True)
    quizzes = models.ManyToManyField(Quiz, related_name='lecture')

class Material(models.Model):
    # can be a doc, video, slide. will be embed using open embed api in page.
    docs = models.FileField(verbose_name=_(u'Attachments'),
                                  upload_to='attachments')
    # is associated with any course/unit/lecture
    session = models.ManyToManyField(Session, related_name='used_in')

# add a separate model for video links, a hack for Vimeo but will be merged later.
# can be used with oembed or popcorn.js
class Vimeo(models.Model):
    link = models.URLField()
    session = models.ForeignKey(Session)
    
class Enrolment(models.Model):
    student = models.ForeignKey(User)
    session = models.ForeignKey(Session)
    completion = PercentField(default=0)
    enrolment_date = models.DateTimeField(_('When was the enrolment made'), auto_now_add=True)
