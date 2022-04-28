# Generated by Django 4.0.4 on 2022-04-28 05:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='INode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'INodes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('inode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FSAPI.inode')),
                ('content', models.CharField(max_length=4096)),
            ],
            options={
                'db_table': 'Documents',
            },
            bases=('FSAPI.inode',),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('inode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='FSAPI.inode')),
            ],
            options={
                'db_table': 'Folders',
            },
            bases=('FSAPI.inode',),
        ),
        migrations.AddField(
            model_name='inode',
            name='topics',
            field=models.ManyToManyField(to='FSAPI.topic'),
        ),
        migrations.AddField(
            model_name='inode',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FSAPI.folder'),
        ),
        migrations.AddIndex(
            model_name='inode',
            index=models.Index(fields=['parent', 'name'], name='INodes_parent__14ba2d_idx'),
        ),
        migrations.AddConstraint(
            model_name='inode',
            constraint=models.UniqueConstraint(fields=('parent', 'name'), name='fsapi_inode_unique_path'),
        ),
    ]
