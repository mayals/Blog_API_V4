# Generated by Django 4.0.3 on 2022-11-23 14:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0006_tag_post_likes_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
