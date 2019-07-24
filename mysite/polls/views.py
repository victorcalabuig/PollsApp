from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist 	
from django.views import generic
from django.utils import timezone


from .models import Question, Choice



# Create your views here.
def only_reps(numbers):
	"""
	takes a list of numbers as an argument and returns
	a new list containing only the numbers that appear 
	more than once
	"""
	answer = []
	start = 0
	for a in numbers:
		start += 1
		for b in numbers[start:]:
			if (a == b and a not in answer):
				answer.append(a)
	return answer


def questions_with_2_plus_choices(self):
	"""
	Creates a list that contains the id´s of 
	questions which have 2 or more choices.
	"""
	q_ids = []
	for choice in Choice.objects.all():
		q_ids.append(choice.question_id)
	return only_reps(q_ids)


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""
		Excludes questions with future publication dates, 
		and those with less than 1 choice.
		"""
		question_ids = questions_with_2_plus_choices(self)
		return Question.objects.filter(
			pub_date__lte=timezone.now()
			).filter(id__in=question_ids).order_by(
			'-pub_date')[:5]




class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		"""
		Excludes questions with future publication dates, 
		and those with less than 1 choice.
		"""
		question_ids = questions_with_2_plus_choices(self)
		return Question.objects.filter(
			pub_date__lte=timezone.now()).filter(
			id__in=question_ids)	




class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
	def get_queryset(self):
		"""
		Exclude questions that aren't published yet and that 
		have no choices.
		"""
		question_ids = questions_with_2_plus_choices(self)
		return Question.objects.filter(
			pub_date__lte=timezone.now()).filter(
			id__in=question_ids)




def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
        })
	else:
		selected_choice.votes += 1
		selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




	# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	
# 	context = {
# 		'latest_question_list': latest_question_list,
# 	}
# 	return render(request, 'polls/index.html', context)

# def detail(request, question_id):
# 	"""try: 
# 		question = Question.objects.get(pk=question_id)
# 	except Question.DoesNotExist:
# 		raise Http404("Question does not exist")
# 	return render(request, 'polls/detail.html', {'question': question})"""
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/detail.html', {'question': question})
	
# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, 'polls/results.html', {'question': question})