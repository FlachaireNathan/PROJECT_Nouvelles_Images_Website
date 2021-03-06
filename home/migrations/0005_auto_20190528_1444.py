# Generated by Django 2.2.1 on 2019-05-28 12:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20190528_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childanswer',
            name='threadAnswer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.ThreadAnswer'),
        ),
        migrations.AlterField(
            model_name='childanswer',
            name='user_modo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childAnswer_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='childpost',
            name='modification_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='childpost',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Post'),
        ),
        migrations.AlterField(
            model_name='childpost',
            name='user_modo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childpost_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='thread_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Thread'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_modo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thread',
            name='modification_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='thread',
            name='user_modo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='thread_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='creation_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='modification_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='thread_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Thread'),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='user_modo',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='threadanswer_user_modo', to=settings.AUTH_USER_MODEL),
        ),
    ]
