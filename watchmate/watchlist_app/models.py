from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class StreamPlatform(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=70)
    about = models.CharField(max_length=250)
    website = models.URLField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Stream Platforms"


class WatchList(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=80)
    storyline = models.CharField(max_length=400)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name='watchlists')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Watchlists"


class Reviews(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    valid_comment = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    review_watchlist = models.ForeignKey(
        WatchList, on_delete=models.CASCADE, related_name="reviews")

    def __str__(self):
        return str(self.rating) + " / " + self.review_watchlist.title

    class Meta:
        verbose_name_plural = "Watchlist Reviews"
