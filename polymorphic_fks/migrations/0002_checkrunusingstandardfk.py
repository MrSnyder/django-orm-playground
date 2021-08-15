# Generated by Django 3.2.6 on 2021-08-15 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polymorphic_fks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckrunUsingStandardFk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('passed', models.BooleanField()),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.ogcservice')),
            ],
        ),
    ]
