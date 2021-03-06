# Generated by Django 2.2.11 on 2020-03-26 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BisboFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file_name', models.CharField(max_length=100)),
                ('file_type', models.CharField(choices=[('png', 'png'), ('jpg', 'jpg')], default='png', max_length=100)),
                ('file_tag', models.CharField(db_index=True, max_length=1000)),
                ('upload_file', models.FileField(max_length=500, null=True, upload_to='')),
                ('upload_video', models.FileField(max_length=500, null=True, upload_to='')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='files_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bisbo_files',
            },
        ),
    ]
