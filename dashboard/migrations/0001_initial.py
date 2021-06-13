# Generated by Django 2.2.19 on 2021-05-18 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReportFrontPage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "partoftheday_morning",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "partoftheday_afternoon",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "partoftheday_evening",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "partoftheday_other",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "totalchatthismonth",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "totalchatthisday",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "totalchatpermonth_thisyear",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "totalchatpermonth_lastyear",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                (
                    "chats_yesterday",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                (
                    "chats_per_month_lastyear",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
                (
                    "chats_per_month_thisyear",
                    models.CharField(blank=True, max_length=2000, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transcript",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField(blank=True, null=True)),
                ("user", models.CharField(blank=True, max_length=100, null=True)),
                ("lh3ChatID", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "referenceQuestion",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("chat_date", models.DateTimeField(blank=True, null=True)),
                (
                    "counter",
                    models.PositiveIntegerField(blank=True, default=0, null=True),
                ),
            ],
            options={
                "ordering": ("-id",),
            },
        ),
        migrations.AddIndex(
            model_name="transcript",
            index=models.Index(
                fields=["referenceQuestion"], name="dashboard_t_referen_acde3a_idx"
            ),
        ),
    ]
