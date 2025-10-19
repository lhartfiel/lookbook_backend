from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from taggit.managers import TaggableManager
import os


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


def validate_image_file_extension(value):
    """Validate that uploaded file is a supported image format"""
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    if ext not in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension {ext}. Allowed extensions: {", ".join(valid_extensions)}'
        )


def validate_image_file_size(value):
    """Validate that uploaded file is not too large"""
    filesize = value.size
    max_size_mb = 10  # 10MB limit
    max_size_bytes = max_size_mb * 1024 * 1024

    if filesize > max_size_bytes:
        raise ValidationError(
            f"File too large. Size should not exceed {max_size_mb}MB. Current size: {filesize/1024/1024:.1f}MB"
        )


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
    image = models.ImageField(
        upload_to="media/",
        validators=[validate_image_file_extension, validate_image_file_size],
    )
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
