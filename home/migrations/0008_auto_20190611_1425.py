# Generated by Django 2.2.2 on 2019-06-11 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20190604_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childpost',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='thread_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Thread'),
        ),
    ]
