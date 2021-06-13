from lh3.api import *
from dashboard.utils.utils import retrieve_transcript
from django.shortcuts import render
from pprint import pprint as print

from dateutil.parser import parse
from django.http import JsonResponse
from django.http import FileResponse
from django.http import HttpResponse
from django.core.files.base import ContentFile
from os import path
import pathlib
from project_config.settings import BASE_DIR


def get_transcript(request, *args, **kwargs):
    client = Client()
    chat_id = int(kwargs.get("chat_id", None))
    transcript_metadata = client.one("chats", chat_id).get()
    transcript = retrieve_transcript(transcript_metadata, chat_id)
    queue_name = transcript_metadata.get("queue").get("name")
    started_date = parse(transcript_metadata.get("started")).strftime("%Y-%m-%d")

    if request.is_ajax():
        return JsonResponse(transcript, safe=False)
    return render(
        request,
        "transcript/transcript.html",
        {
            "object_list": transcript,
            "queue_name": queue_name,
            "started_date": started_date,
            "chat_id": chat_id,
        },
    )


def download_transcript_in_html(request, *args, **kwargs):
    client = Client()
    chat_id = int(kwargs.get("chat_id", None))
    transcript_metadata = client.one("chats", chat_id).get()
    transcript = retrieve_transcript(transcript_metadata, chat_id)

    url = "https://ca.libraryh3lp.com/dashboard/queues/"
    queue_id = str(transcript_metadata.get("queue").get("accunt_id")) + "/calls/"
    guest_id = (
        str(transcript_metadata.get("guest").get("jid"))
        + "/"
        + str(transcript_metadata.get("guest_id"))
    )
    url + queue_id + guest_id

    content = ["<html><body><h3 align='center'>Transcript</h3><hr/><br/><br>"]
    for msg in transcript:
        this_msg = msg.get("message")
        print(this_msg)
        content.append(this_msg)
    print(content)

    filename = "last-transcript-downloaded.html"
    filepath = str(pathlib.PurePath(BASE_DIR, "tmp_file", filename))

    with open(filepath, "w") as file:
        file.write(" ".join(content))

    return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
