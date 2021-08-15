# Generated by Django 3.2.6 on 2021-08-15 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polymorphic_fks', '0005_checkrunwithmultiplefks'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultiTableBaseCheckrun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('passed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunServiceMetadata',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.servicemetadata')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunOgcService',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.ogcservice')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunLayerMetadata',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.layermetadata')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunLayer',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.layer')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunFeatureTypeMetadata',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.featuretypemetadata')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunFeatureType',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.featuretype')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
        migrations.CreateModel(
            name='MultiTableCheckrunDatasetMetadata',
            fields=[
                ('multitablebasecheckrun_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polymorphic_fks.multitablebasecheckrun')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polymorphic_fks.datasetmetadata')),
            ],
            bases=('polymorphic_fks.multitablebasecheckrun',),
        ),
    ]