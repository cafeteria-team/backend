# Generated by Django 3.2.9 on 2022-05-31 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0001_initial'),
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='noticeadmin',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='생성자'),
        ),
        migrations.AddField(
            model_name='notice',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='생성자'),
        ),
        migrations.AddField(
            model_name='notice',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notice', to='store.store', verbose_name='업체'),
        ),
    ]