# Generated by Django 5.0.7 on 2024-07-25 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_produto_compostos_alter_produto_origem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, upload_to='app/static/imagens'),
        ),
    ]
