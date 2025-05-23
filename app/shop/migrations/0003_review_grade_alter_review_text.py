# Generated by Django 4.2.20 on 2025-05-07 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_galery_options_alter_product_options_review"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="grade",
            field=models.CharField(
                blank=True,
                choices=[
                    ("5", "Отлично"),
                    ("4", "Хорошо"),
                    ("3", "Нормально"),
                    ("2", "Плохо"),
                    ("1", "Ужасно"),
                ],
                max_length=20,
                null=True,
                verbose_name="Оценка",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="text",
            field=models.TextField(verbose_name="Текст"),
        ),
    ]
