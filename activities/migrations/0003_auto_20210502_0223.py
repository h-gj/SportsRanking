# Generated by Django 3.1.2 on 2021-05-02 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('activities', '0002_auto_20210502_0148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'activities'},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='activity_duration',
        ),
        migrations.AddField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user'),
        ),
    ]
