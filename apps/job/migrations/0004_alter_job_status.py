# Generated by Django 5.1.1 on 2024-09-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0003_application"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("published", "Published"),
                    ("closed", "Closed"),
                ],
                max_length=10,
            ),
        ),
    ]
