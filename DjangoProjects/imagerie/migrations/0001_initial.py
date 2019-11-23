# Generated by Django 2.2.5 on 2019-11-23 00:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='imagerie.ContentImage')),
            ],
        ),
        migrations.CreateModel(
            name='Loss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Optimizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RankTaxon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('tax_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('found_in_ncbi', models.BooleanField(default=True)),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='imagerie.RankTaxon')),
                ('sup_taxon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='imagerie.Taxon')),
            ],
        ),
        migrations.CreateModel(
            name='TypeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('taxon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='imagerie.Taxon')),
                ('latin_name', models.CharField(max_length=50)),
                ('vernacular_name', models.CharField(max_length=50)),
            ],
            bases=('imagerie.taxon',),
        ),
        migrations.CreateModel(
            name='SubmittedImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='imagerie.Image')),
            ],
            bases=('imagerie.image',),
        ),
        migrations.AddField(
            model_name='image',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='imagerie.TypeImage'),
        ),
        migrations.CreateModel(
            name='CNNArchitecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('model_code', models.FileField(upload_to='models_scripts')),
                ('loss', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='imagerie.Loss')),
                ('optimizer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='imagerie.Optimizer')),
            ],
        ),
        migrations.CreateModel(
            name='CNN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('accuracy', models.DecimalField(decimal_places=3, max_digits=4)),
                ('name', models.CharField(max_length=50)),
                ('learning_data', models.FilePathField(allow_folders=True, null=True)),
                ('available', models.BooleanField(default=False)),
                ('architecture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='imagerie.CNNArchitecture')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pos', models.IntegerField()),
                ('cnn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagerie.CNN')),
                ('specie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='imagerie.Specie')),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence', models.DecimalField(decimal_places=3, max_digits=4)),
                ('cnn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagerie.CNN')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagerie.SubmittedImage')),
                ('specie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imagerie.Specie')),
            ],
        ),
        migrations.CreateModel(
            name='GroundTruthImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='imagerie.Image')),
                ('specie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='imagerie.Specie')),
            ],
            bases=('imagerie.image',),
        ),
        migrations.AddField(
            model_name='cnn',
            name='classes',
            field=models.ManyToManyField(related_name='_cnn_classes_+', through='imagerie.Class', to='imagerie.Specie'),
        ),
        migrations.AddField(
            model_name='cnn',
            name='training_images',
            field=models.ManyToManyField(related_name='cnns_trained_on', to='imagerie.GroundTruthImage'),
        ),
    ]
