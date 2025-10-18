from django.db import models
from django.utils.translation import gettext_lazy as _  # Missing
from taggit.managers import TaggableManager


"""
Tuples for choice options
"""

HAIR_LENGTH = [("SHORT", "Short"), ("MEDIUM", "Medium"), ("LONG", "Long")]

HAIR_TEXTURE = [
    ("STRAIGHT", "Straight"),
    ("WAVY", "Wavy"),
    ("CURLY", "Curly"),
    ("COILY", "Coily"),
]

HAIR_THICKNESS = [("FINE", "Fine"), ("MEDIUM", "Medium"), ("THICK", "Thick")]

IMAGE_TYPE = [
    ("BEFORE", "Before"),
    ("AFTER", "After"),
]

IMAGE_VIEW = [
    ("SIDE", "Side"),
    ("FRONT", "Front"),
    ("BACK", "Back"),
]
MAINTENANCE_CHOICES = [("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")]


class Style(models.Model):
    """
    Individual Style linked to a specific Hair Stylist
    """

    client_permission = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(
        help_text="Optional description for the style", blank=True
    )
    length = models.CharField(
        choices=HAIR_LENGTH,
        max_length=10,
        default="SHORT",
    )
    maintenance = models.CharField(
        choices=MAINTENANCE_CHOICES,
        max_length=10,
        default="LOW",
    )
    texture = models.CharField(
        choices=HAIR_TEXTURE,
        max_length=10,
        default="STRAIGHT",
    )
    thickness = models.CharField(
        choices=HAIR_THICKNESS,
        max_length=10,
        default="FINE",
    )
    stylist_name = models.CharField(max_length=200, blank=False)
    title = models.CharField(
        max_length=350, help_text="Unique name to describe the style"
    )
    tags = TaggableManager(
        help_text="Add any additional tags like 'blonde' for hair color", blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Style")
        verbose_name_plural = _("Styles")


class Image(models.Model):
    image = models.ImageField(upload_to="media/")
    image_alt = models.CharField(
        help_text="Provide alt text for the image", max_length=350
    )
    style = models.ForeignKey(Style, models.CASCADE, related_name="style_image")
    type = models.CharField(
        choices=IMAGE_TYPE,
        max_length=10,
        default="BEFORE",
    )
    view = models.CharField(
        choices=IMAGE_VIEW,
        max_length=10,
        default="FRONT",
    )

    def __str__(self):
        return self.image_alt

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

        # - Implement Style model with UUID primary key, stylist name, maintenance level
        # - Add description field and timestamps
        # - Set up many-to-many relationship with Image model and TaggableManager for tags
