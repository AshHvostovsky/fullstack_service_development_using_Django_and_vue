from django.http import HttpResponse
from django.views import View       
from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from missions.models import Mission

# Create your views here.
class ShowMissionsView(TemplateView):
    template_name = "missions/show_missions.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["missions"] = Mission.objects.all()
        missions = Mission.objects.all()
        return context
