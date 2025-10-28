from django.core.management.base import BaseCommand
from styles.models import Style
from styles.vector_search import VectorSearchService

class Command(BaseCommand):
    help = 'Index all existing styles in Pinecone'

    def handle(self, *args, **options):
        vector_service = VectorSearchService()

        styles = Style.objects.all()
        total_styles = styles.count()

        self.stdout.write(f"Indexing {total_styles} styles...")

        success_count = 0
        for i, style in enumerate(styles, 1):
            self.stdout.write(f"Processing style {i}/{total_styles}: {style.title}")

            if vector_service.index_style(style):
                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Indexed: {style.title}")
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"❌ Failed to index: {style.title}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Indexing complete! {success_count}/{total_styles} styles indexed successfully."
            )
        )
