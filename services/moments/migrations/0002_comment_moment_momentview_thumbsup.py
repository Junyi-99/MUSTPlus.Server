# Generated by Django 3.0b1 on 2020-04-27 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0002_loginrecord_student_takecourse'),
        ('moments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('thumbs_up', models.IntegerField()),
                ('publish_time', models.DateTimeField()),
                ('visible', models.BooleanField()),
                ('pics', models.TextField()),
                ('forwarding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moments.Moment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbsUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbs_time', models.DateTimeField()),
                ('moment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moments.Moment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moments_thumbsup_related', related_query_name='moments_thumbsups', to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='MomentView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moments.Moment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moments_momentview_related', related_query_name='moments_momentviews', to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('publish_time', models.DateTimeField()),
                ('visible', models.BooleanField()),
                ('forwarding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='moments.Comment')),
                ('moment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moments.Moment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moments_comment_related', related_query_name='moments_comments', to='student.Student')),
            ],
        ),
    ]
