from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Question, Choice


class IndexView(generic.ListView):
    """
    The landing page of the website. This page displays all available polls. User can select a poll of their choice to
    vote.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the five most recent published polls."""
        return Question.objects.filter(start_date__lte=timezone.now()).order_by('-start_date')[:5]


class DetailView(generic.DetailView):
    """
    The detail page enables users to vote on the given choices.
    """
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Question.objects.filter(start_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """
    The result page displays the result of a poll.
    """
    model = Question
    template_name = 'polls/results.html'


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
