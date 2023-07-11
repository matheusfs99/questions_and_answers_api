from django.db import migrations
from django.contrib.auth.models import Group, Permission


def create_groups_and_permissions(apps, schema_editor):
    teacher_group, _ = Group.objects.get_or_create(name="Teacher")
    student_group, _ = Group.objects.get_or_create(name="Student")

    permission_names = [
        "view_activity", "view_questions", "view_answers",
        "add_activity", "add_questions", "add_answers",
        "change_activity", "change_questions", "change_answers",
        "cant_view_answer_is_correct",
    ]
    permissions = Permission.objects.filter(codename__in=permission_names)

    teacher_group.permissions.set(permissions)
    student_group.permissions.set(permissions.exclude(codename="view_partial_model"))


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0004_create_permission_to_view_answer_is_correct"),
    ]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
