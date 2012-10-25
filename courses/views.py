from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.utils import timezone
from django.template.defaultfilters import slugify

from quiz.models import *
from courses.models import *
from courses.forms import *
from courses.decorators import professor

def course_create(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        course = course_form.save()
        return HttpResponseRedirect(reverse('courses.views.course', args=(course.slug,)))
    else:
        course_form = CourseForm()
        c = {'session_form': course_form }
        c.update(csrf(request))
        return render_to_response('courses/session_edit.html', c)
        
def course(request, name):
    course = get_object_or_404(Course, slug=name)
    return render_to_response('courses/course.html', {'course': course })

@professor
def course_edit(request, name):
    course = get_object_or_404(Course, slug=name)
    if request.method == 'POST':
        session_form = CourseForm(request.POST, instance=course)
        session_form.save()
        #todo: error handling
        return HttpResponseRedirect(reverse('courses.views.course', args=(course.slug,)))
    else:
        session_form = CourseForm(instance=course)
        c = {'session_form': session_form }
        c.update(csrf(request))
        return render_to_response('courses/session_edit.html', c)
    
@professor
def course_stats(request, name):
    pass

def unit_create(request, name):
    if request.method == 'POST':
        unit_form = UnitForm(request.POST)
        unit = unit_form.save(commit=False)
        unit.slug = slugify(unit.title)
        unit.save()
        return HttpResponseRedirect(reverse('courses.views.unit', args=(unit.slug,)))
    else:
        course = get_object_or_404(Course, slug=name)
        unit_form = UnitForm(initial={'course' : course})
        c = {'session_form': unit_form }
        c.update(csrf(request))
        return render_to_response('courses/session_edit.html', c)

def unit(request, name):
    unit = get_object_or_404(Unit, slug=name)
    return render_to_response('courses/unit.html', {'unit': unit })

def unit_edit(request, name):
    unit = get_object_or_404(Unit, slug=name)
    if request.method == 'POST':
        session_form = UnitForm(request.POST, instance=unit)
        session_form.save()
        #todo: error handling
        return HttpResponseRedirect(reverse('courses.views.unit', args=(unit.slug,)))
    else:
        session_form = UnitForm(instance=unit)
        c = {'session_form': session_form }
        c.update(csrf(request))
        return render_to_response('courses/session_edit.html', c)

def lecture(request, name):
    lecture = get_object_or_404(Lecture, slug=name)
    return render_to_response('courses/lecture.html', {'lecture': lecture })

def lecture_create(request, name):
    pass

def lecture_edit(request, name):
    lecture = get_object_or_404(Lecture, slug=name)
    if request.method == 'POST':
        session_form = LectureForm(request.POST, instance=lecture)
        session_form.save()
        #todo: error handling
        return HttpResponseRedirect(reverse('courses.views.lecture', args=(lecture.slug,)))
    else:
        session_form = LectureForm(instance=lecture)
        c = {'session_form': session_form }
        c.update(csrf(request))
        return render_to_response('courses/session_edit.html', c)

