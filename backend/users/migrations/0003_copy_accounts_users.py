from django.db import migrations, connection
from django.utils import timezone


def copy_accounts_users(apps, schema_editor):
    """
    Copy rows from accounts_user -> users_user if the accounts_user table exists.
    Conservative: skips usernames that already exist in users_user.
    """
    User = apps.get_model('users', 'User')

    # portable check for table existence
    try:
        table_names = connection.introspection.table_names()
    except Exception:
        # if introspection fails, abort
        return

    if 'accounts_user' not in table_names:
        return

    with connection.cursor() as cursor:
        # Select commonly used fields — extend if your accounts_user has extra columns to preserve.
        try:
            cursor.execute("""
                SELECT username, password, email, first_name, last_name,
                       is_staff, is_superuser, is_active, date_joined, role
                FROM accounts_user
            """)
        except Exception:
            # If schema differs or columns missing, abort copy (no-op).
            return
        rows = cursor.fetchall()

    for row in rows:
        # Unpack safely; if the row has fewer columns this will raise and skip.
        try:
            (username, password, email, first_name, last_name,
             is_staff, is_superuser, is_active, date_joined, role) = row
        except Exception:
            continue

        # Skip if username already exists in users_user
        if User.objects.filter(username=username).exists():
            continue

        defaults = {
            'password': password or '',
            'email': email or '',
            'first_name': first_name or '',
            'last_name': last_name or '',
            'is_staff': bool(is_staff),
            'is_superuser': bool(is_superuser),
            'is_active': bool(is_active),
            'date_joined': date_joined or timezone.now(),
            'role': role or 'student',
        }

        try:
            # Create new User row preserving hashed password (do NOT call set_password here).
            User.objects.create(username=username, **defaults)
        except Exception:
            # ignore problematic rows and continue
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_announcement'),
    ]

    operations = [
        migrations.RunPython(copy_accounts_users, reverse_code=migrations.RunPython.noop),
    ]
