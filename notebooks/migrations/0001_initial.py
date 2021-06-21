# Generated by Django 3.2.4 on 2021-06-21 10:30

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import notebooks.models.notebook_file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NotebookFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')),
                ('file', models.FileField(upload_to='notebooks/', validators=[notebooks.models.notebook_file.validate_txt_file_extension], verbose_name='فایل جزوه')),
                ('name', models.CharField(max_length=256, verbose_name='نام جزوه')),
            ],
            options={
                'verbose_name': 'فایل جزوه',
                'verbose_name_plural': 'فایل های جزوات',
            },
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='آیا حذف شده است؟')),
                ('is_archived', models.BooleanField(default=False, verbose_name='آیا آرشیو شده است؟')),
                ('text', models.TextField(verbose_name='متن جزوه')),
                ('model_created', models.BooleanField(default=False, verbose_name='مدلش ساخته شده است؟')),
                ('notebook_file', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='notebook', to='notebooks.notebookfile', verbose_name='فایل جزوه')),
            ],
            options={
                'verbose_name': 'جزوه',
                'verbose_name_plural': 'جزوات',
            },
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
