# Generated by Django 3.2.9 on 2022-05-03 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_store_price'),
        ('notice', '0002_notice_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='store',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notice', to='store.store', verbose_name='업체'),
        ),
    ]