# Generated by Django 3.0b1 on 2020-04-27 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbs_up', models.IntegerField(default=0)),
                ('thumbs_down', models.IntegerField(default=0)),
                ('rank', models.FloatField(default=2.5)),
                ('content', models.TextField()),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=32)),
                ('course_class', models.CharField(max_length=32)),
                ('name_zh', models.TextField()),
                ('name_en', models.TextField(null=True)),
                ('name_short', models.CharField(max_length=30, null=True)),
                ('credit', models.CharField(max_length=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ftp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('port', models.IntegerField()),
                ('username', models.TextField()),
                ('password', models.TextField()),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intake', models.IntegerField(default=0)),
                ('date_begin', models.DateField()),
                ('date_end', models.DateField()),
                ('time_begin', models.TimeField()),
                ('time_end', models.TimeField()),
                ('day_of_week', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ThumbsDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbs_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThumbsUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbs_time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Comment')),
            ],
        ),
    ]