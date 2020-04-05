from django.contrib import admin
from datetime import datetime
from django.urls import reverse
from bisbo_files.models import BisboFile, UserDownloadedFile
from django.contrib import messages
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from utils.s3_file_upload import S3Connection
from django.core.files.storage import FileSystemStorage


class BisboFileAdmin(admin.ModelAdmin):
    search_fields = ('file_name', 'file_tag')
    list_display = ('file_tag', 'image_tag')
    list_filter = ('file_type',)
    fieldsets = (
        (None, {'fields': ('file_name', 'file_type', 'file_tag', 'upload_file', 'upload_video')}),
    )

    def get_queryset(self, request):
        self.full_path = request.get_full_path()
        qs = super(BisboFileAdmin, self).get_queryset(request)
        self.request_obj = request
        return qs

    def image_tag(self, obj):
        download_button = True
        minimum_download = 0
        # 'width="250" height="200" ' '<a class="button" href="{}">Deposit</a>'
        if self.request_obj:
            current_user = self.request_obj.user
            minimum_download = current_user.minimum_download
            if current_user.is_superuser:
                today = datetime.now().date()
                download_count = current_user.downloaded_files.filter(bisbo_file=obj, created__date=today).count()
                if download_count > minimum_download:
                    download_button = False
        if obj.upload_file:
            if download_button:
                return format_html("""<div style="width: 90%;">
                     <table style="width: 80%;">
                     <tbody>
                     <tr>
                     <td><img width="300" height="250" src="{0}"/> </td>
                     </tr>
                     <tr>
                     <td width="10%"><a class="button" href="{1}">Download</a></td>`
                     <td width="20%">Minimum download: {2}</td>`
                     </tr>
                     </tbody>
                     </table>
                     </div>""".format(obj.upload_file, reverse('file-download', args=[obj.pk, self.request_obj.user.id,
                                                                                      ]), minimum_download))
            else:
                return format_html("""<div>
                                     <table style="width: 100%;">
                                     <tbody>
                                     <tr>
                                     <td><img width="250" height="200" src="{0}"/> </td>
                                     </tr>
                                     <tr>
                                     <td width="10%">Minimum download Done</td>`
                                     <td width="20%">Minimum download: {1}</td>`
                                     </tbody>
                                     </table>
                                     </div>""".format(obj.upload_file, minimum_download))
        return obj.upload_file

    image_tag.short_description = 'Image'

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            self.request_obj = request
            return super(BisboFileAdmin, self).changeform_view(request, object_id, form_url, extra_context)
        except Exception as e:
            print("dddddddddddd", e.__str__())
            self.message_user(request, e, level=messages.ERROR)
            return HttpResponseRedirect(request.path)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user

        file_url = video_url = ""
        file_tag = obj.file_tag.lower().replace(" ", "-")

        # # File upload
        try:
            upload_file = request.FILES["upload_file"]
            file_path = '/code/static/' + upload_file.name.lower().replace(" ", "-")
            with open(file_path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)
            # file_lower_name = obj.upload_file.name.lower().replace(" ", "-")
            # obj.upload_file = file_lower_name
            # file_name = f'{file_tag}_{file_lower_name}'
            # file_data = {"directory": "files/", "file_name": file_name}
            # file_url = S3Connection().upload(file_data, obj.upload_file)
            # obj.upload_file = file_url
        except FileNotFoundError:
            pass

        # Video upload
        try:
            upload_video = request.FILES["upload_video"]
            file_path = '/code/static/' + obj.upload_video.name.lower().replace(" ", "-")
            with open(file_path, 'wb+') as destination:
                for chunk in upload_video.chunks():
                    destination.write(chunk)
            obj.upload_video = file_path
        except FileNotFoundError:
            pass

        super(BisboFileAdmin, self).save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if request.user.user_permissions.filter(codename='delete_bisbofile').exists():
            return True
        return False


class UserDownloadedFileAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'bisbo_file__file_tag',
                     'bisbo_file__file_name')
    list_display = ('created_date', 'user', 'bisbo_file')
    list_filter = ('user',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(BisboFile, BisboFileAdmin)
admin.site.register(UserDownloadedFile, UserDownloadedFileAdmin)
