from django.contrib import admin
from django.db import models
from chosen import forms as chosenforms

from quiz.models import  Quiz, MultipleChoiceAnswer, MultipleChoice, QuizInstance, UserResponse

class QuizAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}
	
	radio_admin_fields = {'status': admin.VERTICAL}
	
	list_display = ('title', 'status',)
	list_filter = ('status',)
	search_fields = ('title', 'description',)
	filter_vertical = ('questions',)
	formfield_overrides = {
		models.ManyToManyField: {'widget' : chosenforms.ChosenSelectMultiple },
	}

class MultipleChoiceAdmin(admin.ModelAdmin):
	filter_vertical = ('choices','correct_answer',)
	prepopulated_fields = {'slug': ('question',)}

admin.site.register(Quiz, QuizAdmin)
admin.site.register(MultipleChoiceAnswer)
admin.site.register(MultipleChoice, MultipleChoiceAdmin)
admin.site.register(QuizInstance)
admin.site.register(UserResponse)
