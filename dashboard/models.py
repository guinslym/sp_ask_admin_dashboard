from django.db import models
from django.urls import reverse, reverse_lazy

class ReportFrontPage(models.Model):
    partoftheday_morning = models.PositiveIntegerField(blank=True, null=True)
    partoftheday_afternoon = models.PositiveIntegerField(blank=True, null=True)
    partoftheday_evening = models.PositiveIntegerField(blank=True, null=True)
    partoftheday_other = models.PositiveIntegerField(blank=True, null=True)
    totalchatthismonth = models.PositiveIntegerField(blank=True, null=True)
    totalchatthisday = models.PositiveIntegerField(blank=True, null=True)
    totalchatpermonth_thisyear = models.CharField(max_length=1000, blank=True, null=True)
    totalchatpermonth_lastyear = models.CharField(max_length=1000, blank=True, null=True)
    chats_yesterday = models.CharField(max_length=2000, blank=True, null=True)
    chats_per_month_lastyear = models.CharField(max_length=2000, blank=True, null=True)
    chats_per_month_thisyear = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self.partoftheday_morning)

class Transcript(models.Model):
    message = models.TextField(blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    lh3ChatID = models.PositiveIntegerField(blank=True, null=True)
    referenceQuestion = models.BooleanField(blank=True, null=True, default=False)
    chat_date = models.DateTimeField(blank=True, null=True)
    counter =  models.PositiveIntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('transcript_detail', kwargs={'pk': self.pk})

    class Meta:
            ordering = ('-id',)
            indexes = [
            models.Index(fields=['referenceQuestion']),
        ]