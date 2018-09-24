# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView

from .models import Choice, Question


class Index(TemplateView):
    template_name = 'polls/index.html'

    def get_context_data(self, **kwargs):
        super(Index, self).get_context_data()
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        kwargs['latest_question_list'] = latest_question_list
        return kwargs


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/details.html', {'question': question})


def results(request, question_id):
    # no_of_votes = Question.objects.get(pk=question_id)
    # no_of_votes.choice_set.get()
    response = "%s other people also opted for this choice."
    return HttpResponse(response % question_id)


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
    return HttpResponseRedirect(reverse('polls:results', args=(selected_choice.votes,)))
    # return HttpResponseRedirect('/result/',
    #                             [(Choice.objects.get(i.id).choice_text, Choice.objects.get(i.id).votes) for i in
    #                              question.choice_set.all()])
