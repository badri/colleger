'''
TODO:
1. full AJAX of quiz crud with answers, questions.
2. users can add questions without correct answer, warning will be issued.
3. a quiz cannot be put to use without having all the solutions as correct.
4. check if same question is added again.
'''
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.utils import timezone, simplejson
from quiz.models import *
from quiz.forms import *
from django.template.defaultfilters import slugify

from courses.decorators import professor

def create_user_response(user_response, answers):
	user_response.response=[MultipleChoiceAnswer.objects.get(pk=x) for x in answers]	
	user_response.save()

def questions_list(request):
	questions = MultipleChoice.objects.all()
	return render_to_response('quiz/question_list.html', {'questions': questions })

def question(request, id, slug):
	question = MultipleChoice.objects.get(pk=id)
	return render_to_response('quiz/question.html', {'question': question })

def create_quiz(request, id):
	# todo: put this as a form
	quiz = get_object_or_404(Quiz, pk=id)
	# check if no. of instances have been crossed.
	quiz_instance = QuizInstance(taker=request.user, quiz=quiz)
	# todo: check if instance already exists, retrieve it
	quiz_instance.save()
	return HttpResponseRedirect(reverse('quiz.views.quiz', args=(quiz_instance.pk,)))


def quiz(request, id):
	question_number = 0
	quiz_instance = QuizInstance.objects.get(pk=id)
	quiz = quiz_instance.quiz
	if quiz.get_instances_since_month(user=request.user) > quiz.no_of_takes_per_month:
		message = u'''
                          Hi %s, you have exceeded the number of attempts(%d) for the %s for this month.
                          This quiz will be placed in your queue till next month.
                          ''' % (request.user, quiz.no_of_takes_per_month, quiz)
		return render_to_response('quiz/message.html', {'message': message})
	if request.method == 'POST':
		# save response
		post_data = request.POST
		print post_data
		question_id = int(post_data['question_number'])
		user_response = UserResponse(quiz_instance=quiz_instance, question=quiz.get_question(question_id), time_taken_delta = timezone.now())
		user_response.save()
		create_user_response(user_response, post_data['choices'])
		question_number =  question_id + 1
		if question_number >= quiz.question_count:
			# compute score and results
			quiz_instance.score = sum([int(x.is_correct) for x in quiz_instance.get_responses])
			quiz_instance.complete = True
			quiz_instance.save()
			return HttpResponseRedirect(reverse('quiz.views.result', args=(quiz_instance.pk,)))
	question = quiz.get_question(question_number)
	quiz_form = QuizForm(question)
	# todo: garble question_number using a combination of a key, question, quiz and quiz instance
	c = {'q': question, 'question_form' : quiz_form, 'question_number': question_number }
	c.update(csrf(request))
	return render_to_response('quiz/quiz.html', c)

def result(request, id):
	quiz_instance = get_object_or_404(QuizInstance, pk=id)
	if not quiz_instance.complete:
		raise Http404
	return render_to_response('quiz/quiz_finished.html', {'score': quiz_instance.score })
 
def report(request, id):
	quiz_instance = get_object_or_404(QuizInstance, pk=id)
	if not quiz_instance.complete:
		raise Http404
	pass

@professor
def new_quiz(request):
	if request.method == 'POST':
		# save response
		post_data = request.POST
		#print post_data
		new_quiz = NewQuizForm(request.POST)
		if new_quiz.is_valid():
			print 'valid'
			quiz = new_quiz.save(commit=False)
			quiz.setter = request.user
			quiz.slug = slugify(quiz.title)
			quiz.save()
			return HttpResponseRedirect(reverse('quiz.views.add_question', args=(quiz.pk,)))
		else:
			print new_quiz.errors
		# redirect to add questions
	new_quiz_form = NewQuizForm()
	c = {'new_quiz_form' : new_quiz_form }
	c.update(csrf(request))
	return render_to_response('quiz/new_quiz.html', c)


def add_answer_choice(request):
	if request.is_ajax():
		answer_choice = MultiChoiceAnswerForm()
		response = { 'answer' : answer_choice.as_p() }
		data = simplejson.dumps(response)
		return HttpResponse(data, mimetype="application/json")

def add_new_question(request):
	if request.is_ajax():
		# type = request.POST.get('type')
		multichoice = MultiChoiceForm()
		response = { 'question' : multichoice.as_p() }
		data = simplejson.dumps(response)
		return HttpResponse(data, mimetype="application/json")

def add_question(request, id):
	quiz = get_object_or_404(Quiz, pk=id)
	return render_to_response('quiz/add_question.html', { 'quiz' : quiz})
	
