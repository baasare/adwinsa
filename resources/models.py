from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from adwinsa import settings


class Resource(models.Model):
    LEVEL = (
        ('KG_1', 'Kindergarten 1'),
        ('KG_2', 'Kindergarten 2'),
        ('B_1', 'Basic 1'),
        ('B_2', 'Basic 2'),
        ('B_3', 'Basic 3'),
        ('B_4', 'Basic 4'),
        ('B_5', 'Basic 5'),
        ('B_6', 'Basic 6'),
        ('B_7', 'Basic 7'),
        ('B_8', 'Basic 8'),
        ('B_9', 'Basic 9'),
        ('B_10', 'Basic 10'),
        ('B_11', 'Basic 12'),
        ('B_12', 'Basic 12'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=15, choices=LEVEL)
    strand = models.IntegerField(
        validators=[
            MaxValueValidator(50),
            MinValueValidator(1)
        ]
    )
    sub_strand = models.IntegerField()
    url = models.URLField()

    class Meta:
        ordering = ('-level', 'strand', 'sub_strand')

    def __str__(self):
        return "%s" % self.title
