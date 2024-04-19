# Generated by Django 5.0.4 on 2024-04-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='images/categories/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='size',
            field=models.CharField(choices=[('ICON', 'Иконка'), ('PREVIEW', 'Превью'), ('ORIGINAL', 'Оригинальный')], default='ORIGINAL', max_length=8, verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(upload_to='images/subcategories/', verbose_name='Картинка'),
        ),
        migrations.AddConstraint(
            model_name='productimage',
            constraint=models.UniqueConstraint(fields=('size', 'product'), name='unique_image_size'),
        ),
    ]