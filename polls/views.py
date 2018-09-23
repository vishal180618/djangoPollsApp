# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404
from django.shortcuts import render

from models import Question
from django.template import loader
from django.views.generic import TemplateView


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
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
