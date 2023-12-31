# Generated by Django 4.2.3 on 2023-08-02 17:29

import dj_dynamic_templates.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

try:
    import markdownx.models
    markdownx_exist = True
except ModuleNotFoundError:
    markdownx_exist = False


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('code', models.PositiveBigIntegerField()),
                ('app_name', models.CharField(help_text='In this App, Directory will be created within templates folder', max_length=50, validators=[dj_dynamic_templates.validators.validate_app])),
                ('name', models.CharField(help_text='Will use this name as an Directory name', max_length=50)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': ' DJ Dynamic Template Category',
                'verbose_name_plural': ' DJ Dynamic Template Categories',
                'db_table': 'dj_dynamic_templates__category',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('code', models.PositiveBigIntegerField()),
                ('body_content', markdownx.models.MarkdownxField()) if markdownx_exist else ('body_content', models.TextField()),
                ('style_content', models.TextField(blank=True)),
                ('script_content', models.TextField(blank=True)),
                ('name', models.CharField(help_text='Entered name will treated as template file name, A template file is created with this file name', max_length=50)),
                ('category', models.ForeignKey(help_text='Select the category where you want to save the template', on_delete=django.db.models.deletion.CASCADE, related_name='mail_template_category', to='dj_dynamic_templates.category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dj_dynamic_templates.mailtemplate')),
            ],
            options={
                'verbose_name': 'DJ Dynamic Template - Mail Template',
                'verbose_name_plural': "DJ Dynamic Template - Mail Template's",
                'db_table': 'dj_dynamic_templates__mail_template',
                'permissions': (('can_view_inactive_objects', 'Can view Inactive Objects'), ('can_sync_templates', 'Can Sync Templates'), ('can_view_created_by', 'Can View Created By'), ('can_view_history', 'Can View History')),
                'managed': True,
            },
        ),
    ]
