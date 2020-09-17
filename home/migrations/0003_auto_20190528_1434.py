# Generated by Django 2.2.1 on 2019-05-28 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190528_1148'),
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
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='childAnswer_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='childanswer',
            name='user_op',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='childAnswer_user_op', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='childpost',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Post'),
        ),
        migrations.AlterField(
            model_name='childpost',
            name='user_modo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='childpost_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='childpost',
            name='user_op',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='childpost_user_op', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='thread_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Thread'),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_modo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='post_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='user_op',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='post_user_op', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='thread_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Thread'),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='user_modo',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='threadanswer_user_modo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='threadanswer',
            name='user_op',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='threadanswer_user_op', to=settings.AUTH_USER_MODEL),
        ),
    ]
