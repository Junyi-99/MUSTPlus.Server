# Generated by Django 3.0.6 on 2020-06-03 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0002_comment_course_ftp_schedule_thumbsdown_thumbsup'),
        ('basic', '0002_classroom_department_faculty_major_program'),
        ('student', '0002_loginrecord_student_takecourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbsup',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='thumbsdown',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Comment'),
        ),
        migrations.AddField(
            model_name='thumbsdown',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.ClassRoom'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
        migrations.AddField(
            model_name='ftp',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
        migrations.AddField(
            model_name='ftp',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.Faculty'),
        ),
        migrations.AddField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course'),
        ),
        migrations.AddField(
            model_name='comment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AlterUniqueTogether(
            name='thumbsup',
            unique_together={('student', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='thumbsdown',
            unique_together={('student', 'comment')},
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('course_code', 'course_class')},
        ),
    ]