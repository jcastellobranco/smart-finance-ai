from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("receipts", "0001_initial")]
    operations = [
        migrations.AlterField(
            model_name="receiptupload",
            name="status",
            field=models.CharField(
                max_length=30, default="pending",
                choices=[
                    ("pending", "Pending"), ("processing", "Processing"),
                    ("review", "Needs review"), ("completed", "Completed"),
                    ("failed", "Failed"),
                ],
            ),
        ),
    ]
