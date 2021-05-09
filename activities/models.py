from django.db import models

# Create your models here.


class Activity(models.Model):
    machine_used_per_min = models.IntegerField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    duration = models.IntegerField(null=True, editable=False)
    # activity_duration = models.IntegerField()
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'activities'

    def save(self, *args, **kwargs):
        self.duration = (self.end_at - self.start_at).total_seconds()
        super().save(*args, **kwargs)
