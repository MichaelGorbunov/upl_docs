# Generated by Django 5.1.5 on 2025-01-27 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, help_text='Comment for doc', max_length=150, null=True, verbose_name='Комментарий к документу')),
                ('original_filename', models.CharField(blank=True, help_text='File name', max_length=150, null=True, verbose_name='Имя файла')),
                ('file', models.FileField(upload_to='upload')),
                ('hash_file', models.CharField(blank=True, help_text='File hash', max_length=32, null=True, verbose_name='Хэш файла')),
                ('state_file', models.SmallIntegerField(choices=[(0, 'Документ отклонен'), (1, 'Документ принят'), (2, 'Докумен на проверке')], default=2, help_text='Состояние документа', verbose_name='Состояние документа')),
                ('created_time', models.DateTimeField(auto_now=True, verbose_name='Время создания')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
                'ordering': ['created_time'],
            },
        ),
    ]
