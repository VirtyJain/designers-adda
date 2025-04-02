# Generated by Django 5.1.6 on 2025-04-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='Username')),
                ('password', models.CharField(max_length=20, verbose_name='Password')),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='age',
            field=models.IntegerField(null=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_no',
            field=models.IntegerField(null=True, verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='date_of_birth',
            field=models.DateField(null=True, verbose_name='Date of Birth'),
        ),
    ]
