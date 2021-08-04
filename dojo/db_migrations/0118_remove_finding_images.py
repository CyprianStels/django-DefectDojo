# Generated by Django 3.1.13 on 2021-07-10 00:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def move_images_to_files(apps, schema_editor):
    Finding_model = apps.get_model('dojo', 'Finding')
    FileUpload_model = apps.get_model('dojo', 'FileUpload')
    for finding in Finding_model.objects.filter(images__isnull=False):
        for image in finding.images.all():
            file = FileUpload_model.objects.create(
                title=image.caption if not len(image.caption) else 'Image Migration',
                file=image.image
            )
            finding.files.add(file)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dojo', '0117_usercontactinfo_force_password_reset'),
    ]

    operations = [
        migrations.RunPython(move_images_to_files),
        migrations.CreateModel(
            name='FileAccessToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('size', models.CharField(choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('thumbnail', 'Thumbnail'), ('original', 'Original')], default='medium', max_length=9)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dojo.fileupload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='findingimageaccesstoken',
            name='image',
        ),
        migrations.RemoveField(
            model_name='findingimageaccesstoken',
            name='user',
        ),
        migrations.RemoveField(
            model_name='finding',
            name='images',
        ),
        migrations.DeleteModel(
            name='FindingImage',
        ),
        migrations.DeleteModel(
            name='FindingImageAccessToken',
        ),
    ]