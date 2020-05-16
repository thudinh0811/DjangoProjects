from django.shortcuts import render, get_object_or_404
from .models import Choice, Question
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
#from django.template import loader

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

'''def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ','.join([q.question_text for q in latest_question_list])
    #template = loader.get_template('polls/index.html')
    context = {'latest_question_list':latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    #return HttpResponse("You're looking at question %s."%question_id)
    #try:
        #question = Question.objects.get(pk=question_id)
    #except Question.DoesNotExist:
        #raise Http404("Question does not exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

#def results(request, question_id):
    #response = f"You're looking at the results of question {question_id}."
   # return HttpResponse(response)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})'''

def vote(request, question_id):
    #return HttpResponse("You're voting on question %s."%question_id)
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #redisplay the question voting form
        return render(request, 'polls/detail.html', {
           'question': question,
            'error_message': "You didn't select a choice.",
         })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #always return HttpResponseRedirect after successfully dealing
        #with POST data, prevents data from being posted twice if a user hits Back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        #return last 5 published questions
        """ 
        return last 5 published questions (not including those set to be published in the future)
        """
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self): #exclude future questions
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'