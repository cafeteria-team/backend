# Generated by Django 3.2.9 on 2022-04-17 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_joinfacility_store'),
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notice', to='store.store', verbose_name='업체'),
            preserve_default=False,
        ),
    ]