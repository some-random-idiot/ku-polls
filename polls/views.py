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


class DetailView(generic.DetailView):
    """
    The detail page enables users to vote on the given choices.
    """
    def get_queryset(self):
        """
        Get poll that matches the provided ID.
        """
        return Question.objects.filter(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        super().get(self, request, *args, **kwargs)
        if not self.get_object().can_vote():
            return redirect('polls:index', 'error')
        return render(request, 'polls/detail.html', self.get_context_data())


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
