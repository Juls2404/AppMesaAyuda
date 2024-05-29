# Generated by Django 5.0.6 on 2024-05-29 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appservicios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userTipo',
            field=models.CharField(choices=[('Administrativo', 'Administrativo'), ('Instructor', 'Instructor'), ('Tecnico', 'Tecnico')], db_comment='Tipo de usuario', max_length=15),
        ),
    ]