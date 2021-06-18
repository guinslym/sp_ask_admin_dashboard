from lh3.api import *
from django.views.generic import TemplateView
from dashboard.utils.utils import (
    soft_anonimyzation,
    operatorview_helper,
    Chats,
    retrieve_transcript,
    search_chats,
)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class SearchProfileResultsView(TemplateView):
    """[summary]

    Args:
        TemplateView ([type]): [description]

    Returns:
        [type]: [description]
    """
    template_name = "results/profile.html"

    @csrf_exempt
    def get_context_data(self, **kwargs):
        context = super(SearchProfileResultsView, self).get_context_data(**kwargs)
        context["title"] = "Profile"
        search_value = self.request.GET.get("queue_id")

        client = Client()
        profile = client.one("profiles", int(search_value)).get()
        context["profile"] = profile["content"]
        context["title"] = profile["name"]
        context["queues"] = client.all("queues").get_list()
        context["standalone_link"] = (
            "https://ca.libraryh3lp.com/dashboard/profiles/"
            + str(int(search_value))
            + "?standalone=true"
        )

        return context


def get_this_profile(request, *args, **kwargs):
    """[summary]

    Args:
        request ([type]): [description]

    Returns:
        [type]: [description]
    """
    queue_id = kwargs.get("queue_id", None)
    queue_id = int(queue_id)
    client = Client()
    queues = client.all("queues").get_list()
    title = "Profile"
    profile = None
    if queue_id:
        profile_api = client.one("profiles", int(queue_id)).get()
        profile = profile_api["content"]
        title = profile_api.get("name", None)
        standalone_link = (
            "https://ca.libraryh3lp.com/dashboard/profiles/"
            + str(int(queue_id))
            + "?standalone=true"
        )

        if request.is_ajax():
            return JsonResponse(profile, safe=False)
        return render(
            request,
            "results/profile.html",
            {
                "profile": profile,
                "title": title,
                "standalone_link": standalone_link,
                "queues": queues,
            },
        )
    if request.is_ajax():
        return JsonResponse(queues, safe=False)
    return render(
        request,
        "results/profile.html",
        {"queues": queues, "title": title, "profile": profile},
    )
