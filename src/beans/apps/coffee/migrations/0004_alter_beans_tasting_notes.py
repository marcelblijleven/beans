# Generated by Django 4.0.3 on 2022-03-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0003_tastingnote_beans_variety_beans_tasting_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beans',
            name='tasting_notes',
            field=models.ManyToManyField(null=True, to='coffee.tastingnote'),
        ),
    ]
