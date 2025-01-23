# Generated by Django 5.1.5 on 2025-01-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='tg_chat_id',
            field=models.CharField(blank=True, help_text='Укажите чат ID в Telegram', max_length=50, null=True, verbose_name='TG чат ID'),
        ),
    ]
