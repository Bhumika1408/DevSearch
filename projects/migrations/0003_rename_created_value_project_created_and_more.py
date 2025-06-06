# Generated by Django 5.1.6 on 2025-03-11 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_tag_review_project_tag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='created_value',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='source_code',
            new_name='source_link',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='vaues',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tag',
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, to='projects.tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='vote_ratio',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='vote_total',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
