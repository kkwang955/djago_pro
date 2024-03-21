# Generated by Django 4.2.10 on 2024-03-04 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("User", "0005_usermodel_alter_patient_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patient",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="UserModel",
        ),
    ]