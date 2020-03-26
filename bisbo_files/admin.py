from django.contrib import admin
from bisbo_files.models import BisboFiles
from django.contrib import messages
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from utils.s3_file_upload import S3Connection


class BisboFilesAdmin(admin.ModelAdmin):
    search_fields = ('file_name', 'file_tag')
    list_display = ('file_name', 'file_tag', 'file_type')
    list_filter = ('file_type',)
    fieldsets = (
        (None, {'fields': ('file_name', 'file_type', 'file_tag', 'upload_file', 'upload_video')}),
    )

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            return super(BisboFilesAdmin, self).changeform_view(request, object_id, form_url, extra_context)
        except Exception as e:
            print("dddddddddddd", e.__str__())
            self.message_user(request, e, level=messages.ERROR)
            return HttpResponseRedirect(request.path)

    def save_model(self, request, obj, form, change):
        print("DDDDDDDDDDDVVVVVVVVVVVV")
        import pdb; pdb.set_trace()
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user

        file_url = video_url = ""
        file_tag = obj.file_tag.lower().replace(" ", "-")

        # File upload
        try:
            file_lower_name = obj.upload_file.name.lower().replace(" ", "-")
            file_name = f'{file_tag}_{file_lower_name}'
            file_data = {"directory": "files/", "file_name": file_name}
            file_url = S3Connection().upload(file_data, obj.upload_file)
        except FileNotFoundError:
            pass

        # Video upload
        try:
            video_file_lower_name = obj.upload_video.name.lower().replace(" ", "-")
            video_file_name = f'{file_tag}_{video_file_lower_name}'
            video_data = {"directory": "files/", "file_name": video_file_name}
            video_url = S3Connection().upload(video_data, obj.upload_video)
        except FileNotFoundError:
            pass

        obj.upload_file = file_url
        obj.upload_video = video_url
        super(BisboFilesAdmin, self).save_model(request, obj, form, change)


    def has_delete_permission(self, request, obj=None):
        if request.user.user_permissions.filter(codename='delete_bisbofiles').exists():
            return True
        return False


admin.site.register(BisboFiles, BisboFilesAdmin)
