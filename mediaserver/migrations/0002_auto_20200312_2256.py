# Generated by Django 2.2.10 on 2020-03-12 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediaserver', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediadatabase',
            name='movie_url',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='mediadatabase',
            name='movie_path',
            field=models.FileField(upload_to='movie_storage/'),
        ),
    ]
