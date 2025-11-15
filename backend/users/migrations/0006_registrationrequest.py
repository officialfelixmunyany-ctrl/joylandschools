from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_studentprofile_users_sp_assess_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('parent', 'Parent')], max_length=16)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('country_code', models.CharField(blank=True, max_length=8)),
                ('phone', models.CharField(blank=True, max_length=32)),
                ('address', models.TextField(blank=True)),
                ('birth_month', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('birth_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('birth_year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('heard_about', models.CharField(blank=True, max_length=255)),
                ('agree', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(default='pending', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
