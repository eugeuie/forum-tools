# Generated by Django 3.0.5 on 2020-04-05 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_identifier_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=80)),
                ('full_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=80, null=True)),
                ('last_name', models.CharField(max_length=80, null=True)),
                ('email', models.CharField(max_length=64)),
                ('admission_year', models.PositiveIntegerField()),
            ],
            options={
                'db_table': '_users',
            },
        ),
        migrations.AlterField(
            model_name='message',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.DO_NOTHING, to='board.TashkentMember'),
        ),
        migrations.AlterField(
            model_name='message',
            name='board',
            field=models.ForeignKey(db_column='board', on_delete=django.db.models.deletion.DO_NOTHING, to='board.TashkentBoard'),
        ),
        migrations.AlterField(
            model_name='message',
            name='identifier',
            field=models.ForeignKey(db_column='identifier', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='board.Identifier'),
        ),
        migrations.AlterField(
            model_name='message',
            name='topic',
            field=models.ForeignKey(db_column='topic', on_delete=django.db.models.deletion.DO_NOTHING, to='board.TashkentTopic'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(db_column='user', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='board.User'),
        ),
    ]
