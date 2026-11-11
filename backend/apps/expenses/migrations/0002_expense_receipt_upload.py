from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0001_initial"),
        ("receipts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="receipt_upload",
            field=models.OneToOneField(
                to="receipts.receiptupload",
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name="expense",
            ),
        ),
    ]
