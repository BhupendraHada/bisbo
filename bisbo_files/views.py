from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from bisbo_files.models import UserDownloadedFile


def file_download(request, file_id, user_id):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    if file_id and user_id:
        UserDownloadedFile.objects.create(bisbo_file_id=file_id, user_id=user_id)

    return redirect("/admin/bisbo_files/bisbofile/")