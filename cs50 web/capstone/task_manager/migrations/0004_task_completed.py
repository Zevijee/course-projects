# Generated by Django 4.2.2 on 2023-07-03 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task_manager", "0003_task_date_todo_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="completed",
            field=models.BooleanField(default=False),
        ),
    ]
