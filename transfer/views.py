from django.shortcuts import render

# Create your views here.
from pathlib import Path

from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .models import SharedFile


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")

        if uploaded_file:
            SharedFile.objects.create(
                file=uploaded_file,
                original_name=Path(uploaded_file.name).name,
            )
            return redirect("index")

    files = SharedFile.objects.order_by("-uploaded_at")

    return render(
        request,
        "transfer/index.html",
        {"files": files},
    )


def download_file(request, file_id):
    shared_file = get_object_or_404(SharedFile, pk=file_id)

    try:
        response = FileResponse(
            shared_file.file.open("rb"),
            as_attachment=True,
            filename=shared_file.original_name,
        )
        return response
    except (OSError, ValueError):
        raise Http404("File tidak ditemukan")