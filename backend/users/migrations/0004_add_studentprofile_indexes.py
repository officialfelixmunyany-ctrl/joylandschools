from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_copy_accounts_users'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='studentprofile',
            index=models.Index(fields=['assessment_number'], name='users_sp_assess_idx'),
        ),
        migrations.AddIndex(
            model_name='studentprofile',
            index=models.Index(fields=['admission_number'], name='users_sp_admit_idx'),
        ),
    ]
