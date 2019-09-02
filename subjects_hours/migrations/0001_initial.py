# Generated by Django 2.2.4 on 2019-08-29 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('cod_subject', models.CharField(
                    max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PersonSubject',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('dni_person', models.CharField(max_length=20)),
                ('period', models.CharField(max_length=10)),
                ('typology', models.CharField(max_length=1)),
                ('dedication_hours', models.IntegerField()),
                ('autonomous_hours', models.IntegerField()),
                ('accompaniment_hours', models.IntegerField()),
                ('cod_subject', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='subjects_hours.Subject')),
            ],
            options={
                'unique_together': {('dni_person', 'cod_subject', 'period')},
            },
        ),
    ]