from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice


def index(request, error_message=''):
    """
    The landing page of the website. This page displays all available polls. User can select a poll of their choice to
    vote.
    """
    latest_poll_list = Question.objects.filter(start_date__lte=timezone.now()).order_by('-start_date')
    context = {'latest_poll_list': latest_poll_list, "error_message": error_message}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """
    The detail page enables users to vote on the given choices.
    """
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})
    return redirect('polls:index', 'The poll you tried to access is not available for voting!')


class ResultsView(generic.DetailView):
    """
    The result page displays the result of a poll.
    """
    template_name = 'polls/results.html'
    model = Question


def vote(request, question_id):
    """
    In charge of adding vote count and detecting whether any answer has been selected or not. If no answer is selected
    it redirects the user to the details page along with an error message.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
