# Generated by Django 5.1 on 2024-08-19 14:48

import django.db.models.deletion
import django_jalali.db.models
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_blog_comment_created_0e6ed4_idx_blog_comment_created_0e6ed4_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='بایو')),
                ('photo', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=60, scale=None, size=[500, 500], upload_to='account_images/', verbose_name='تصویر')),
                ('job', models.CharField(blank=True, max_length=250, null=True, verbose_name='شغل')),
            ],
            options={
                'verbose_name': 'اکانت',
                'verbose_name_plural': 'اکانت ها',
            },
        ),
        migrations.RenameIndex(
            model_name='comment',
            new_name='blog_comment_created_0e6ed4_idx',
            old_name='blog_comment_created_0e6ed4_idx',
        ),
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=75, scale=None, size=[500, 500], upload_to='post_image/'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL),
        ),
    ]
