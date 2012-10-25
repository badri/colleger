from django.forms import ModelForm, HiddenInput
from courses.models import Course, Unit, Lecture

class CourseForm(ModelForm):
    class Meta:
        model = Course

class UnitForm(ModelForm):
    class Meta:
        model = Unit
        exclude = ('slug',)
        widgets = {
            'course' : HiddenInput(),
            }

class LectureForm(ModelForm):
    class Meta:
        model = Lecture

