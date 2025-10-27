
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import Style
from .vector_search import VectorSearchService


# Define the receiver
@receiver(post_save, sender=Style)
def styles_changed(sender, instance, **kwargs):
    vector_service = VectorSearchService()
    vector_service.index_style(instance)

@receiver(post_delete, sender=Style)
def styles_deleted(sender, instance, **kwargs):
    vector_service = VectorSearchService()
    vector_service.delete_style(instance)

@receiver(m2m_changed, sender=Style.tags.through)
def tags_changed(sender, instance, action, **kwargs):
  if action in ['post_add', 'post_remove', 'post_clear']:
      vector_service = VectorSearchService()
      vector_service.index_style(instance)
