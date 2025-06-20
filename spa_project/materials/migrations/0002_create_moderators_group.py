from django.db import migrations

def create_moderators_group(apps, schema_editor):
    Group      = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # создаём группу (или получаем, если уже есть)
    moderators, _ = Group.objects.get_or_create(name='moderators')

    # выбираем именно те права, которые нужны модераторам:
    # view и change для моделей Course и Lesson
    perms = Permission.objects.filter(
        content_type__app_label='materials',
        codename__in=[
            'view_course', 'change_course',
            'view_lesson',  'change_lesson',
        ]
    )

    # устанавливаем эти права группе
    moderators.permissions.set(perms)

class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
        ('auth',      '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_moderators_group),
    ]
