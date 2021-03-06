from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from .models import Question, Choice
import logging

previous_choice = []

class IndexView(generic.ListView):
    """ Show a list of polls """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """ return the last five question was published """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    """ Show the question detail"""
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """ return the question detail that published at now """
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    """ Shhow the result of poll """
    model = Question
    template_name = 'polls/results.html'

@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """ Vote the polls question """
    user = request.user
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)

    question = get_object_or_404(Question, pk=question_id)
    try:
        configure()
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        configure()
        return render(request, 'polls/detail.html', {
            'question' : question,
            'error_message' : "Please select a choice.",
        })
    else:
        if len(previous_choice) >= 1:
            if len(previous_choice) == 2 :
                if selected_choice == previous_choice[0] == previous_choice[1] :
                    configure()
                    selected_choice.votes += 1
                    previous_choice.pop(0)
                    previous_choice.append(selected_choice)
                    selected_choice.save()    
            elif selected_choice == previous_choice[0] :
                previous_choice.append(selected_choice)
                return render(request, 'polls/detail.html', {
                    'question' : question,
                    'error_message' : f"You selected '{selected_choice}' already !  Click 'Vote' to vote again",
                })
        else:
            configure()
            selected_choice.votes += 1
            previous_choice.append(selected_choice)
            selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def configure():
    """ Configure loggers and log handlers """
    filehandler = logging.FileHandler("demo.log")
    filehandler.setLevel(logging.NOTSET)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    filehandler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(filehandler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(fmt='%(levelname)-8s %(name)s: %(message)s')
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)


def allowed_vote(request, question_id):
    """ return result if the vote was success """
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, f"You are not allowed to vote this poll.")
        return redirect('polls:index')
        messages.success(request, "Your vote successfully recorded. Thank you.")
        return redirect('polls:results')
