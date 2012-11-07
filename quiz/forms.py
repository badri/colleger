from django import forms
from quiz.models import *
from form_utils.forms import BetterModelForm

class QuizForm(forms.Form):
	choices = forms.ModelChoiceField(queryset=MultipleChoiceAnswer.objects.none(),
					 widget=forms.CheckboxSelectMultiple, required=True, show_hidden_initial=True)

	def __init__(self, question):
		super(QuizForm, self).__init__()
		self.fields['choices'].queryset = question.choices.all()
		self.fields['choices'].empty_label = None

class QuizForm2(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuizForm2, self).__init__(*args, **kwargs)
        self.fields['choices'] = forms.ChoiceField(widget=forms.CheckboxSelectMultiple, choices=[ (x.id, x.answer) for x in question.choices.all()])

class NewQuizForm(BetterModelForm):
	class Meta:
		model = Quiz
		fieldsets = [
			('Create new quiz', {'fields': ['title', 'description', 'status', 'type'] }),
			('Advanced', {
				'classes': ['collapse'],
				'fields': ['allow_skipping', 'allow_jumping', 'backwards_navigation', 'no_of_takes_per_month', 'no_of_instances_per_month',
					   'random_question', 'feedback', 'multiple_takes']
				})]	
		exclude = ('setter', 'slug', 'questions', 'categories',)

class MultiChoiceAnswerForm(forms.ModelForm):
	class Meta:
		model = MultipleChoiceAnswer
