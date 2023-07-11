from django.db import migrations
from django.contrib.auth.models import Permission


def create_custom_permission(apps, schema_editor):
    permission, _ = Permission.objects.get_or_create(
        codename="cant_view_answer_is_correct",
        name="Can't view answer is_correct",
        content_type_id=7,
    )

    model_fields = ["answer_text", "from_question"]
    permission.view_field_names = model_fields
    permission.save()


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0003_activity_created_at_activity_created_by_and_more"),
    ]

    operations = [
        migrations.RunPython(create_custom_permission),
    ]
