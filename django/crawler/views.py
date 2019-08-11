from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import connections
from django.template import loader
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.views.decorators import csrf
from crawler.models import *
import pprint


class IndexView(ListView):
    model = Top100
    template_name = 'crawler/index.html'
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["table_title"] = "猫眼评分Top100"
        context["movies"] = Top100.objects.order_by("-score")
        return context


class MoviesSearchView(ListView):
    model = Top100
    template_name = 'crawler/index.html'
    context_object_name = 'search'

    def get_context_data(self, **kwargs):
        context = super(MoviesSearchView, self).get_context_data(**kwargs)
        context["movies"] = Top100.objects.all()[:10]
        if self.request.GET:
            search_type = self.request.GET['s']
            search_key = self.request.GET['q']
            context["table_title"] = f"{search_key} 查询结果"
            try:
                context["movies"] = []
                if search_type == "title":
                    context["movies"] = Top100.objects.filter(title__contains=search_key).order_by("-score")
                elif search_type == "stars":
                    context["movies"] = Top100.objects.filter(stars__contains=search_key).order_by("-score")
                elif search_type == "score_gt":
                    context["movies"] = Top100.objects.filter(score__gt=float(search_key)).order_by("-score")
                    context["table_title"] = f"评分大于 {float(search_key)} 查询结果"
                elif search_type == "score_lt":
                    context["movies"] = Top100.objects.filter(score__lt=float(search_key)).order_by("-score")
                    context["table_title"] = f"评分小于 {float(search_key)} 查询结果"
                elif search_type == "time_before":
                    context["movies"] = Top100.objects.filter(release_time__lt=search_key).order_by("-release_time")
                    context["table_title"] = f"上映时间 {search_key} 之前的查询结果"
                elif search_type == "time_after":
                    context["movies"] = Top100.objects.filter(release_time__gt=search_key).order_by("-release_time")
                    context["table_title"] = f"上映时间 {search_key} 之后的查询结果"
                if not context["movies"]:
                    context["table_title"] = "本此查询无匹配项目"
            except:
                context["table_title"] = "本此查询条件有误"

        return context


def show_movies(request):
    table_title = "猫眼Top100"
    movies_query = Top100.objects.all()
    if movies_query:
        movies = [model_to_dict(i) for i in Top100.objects.all()]
        movies = [i for i in movies]
    return render(request, 'crawler/index.html',
                  {'table_title': table_title, 'movies': movies})
