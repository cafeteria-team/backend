# Generated by Django 3.2.9 on 2022-04-10 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_joinfacility_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joinfacility',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_facility', to='store.store', verbose_name='업체'),
        ),
    ]