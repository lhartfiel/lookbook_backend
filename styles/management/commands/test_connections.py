from django.core.management.base import BaseCommand
from django.conf import settings
from openai import OpenAI
import os


class Command(BaseCommand):
    help = "Test Pinecone and OpenAI connections"

    def handle(self, *args, **options):
        self.stdout.write("Testing API connections...")

        # Test OpenAI
        self.test_openai()

        # Test Pinecone
        self.test_pinecone()

        self.stdout.write(self.style.SUCCESS("Connection tests completed!"))

    def test_openai(self):
        try:
            self.stdout.write("Testing OpenAI connection...")

            # Initialize OpenAI client (new v1.x syntax)
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            # Test with a simple embedding
            response = client.embeddings.create(
                model="text-embedding-ada-002", input="test connection"
            )

            embedding = response.data[0].embedding
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ OpenAI connected! Embedding dimension: {len(embedding)}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ OpenAI connection failed: {str(e)}")
            )

    def test_pinecone(self):
        try:
            self.stdout.write("Testing Pinecone connection...")

            # Use new Pinecone v3+ API
            from pinecone import Pinecone

            # Create Pinecone client instance
            pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

            self.stdout.write(
                f"Debug - API Key: {os.getenv('PINECONE_API_KEY')[:10]}..."
            )
            self.stdout.write(f"Debug - Index Name: {os.getenv('PINECONE_INDEX_NAME')}")

            # List all available indexes
            indexes_response = pc.list_indexes()
            available_indexes = [idx.name for idx in indexes_response]

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Pinecone connected! Available indexes: {available_indexes}"
                )
            )

            # Test access to specific index
            index_name = os.getenv("PINECONE_INDEX_NAME")
            if index_name and index_name in available_indexes:
                index = pc.Index(index_name)
                stats = index.describe_index_stats()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Index '{index_name}' accessible! Stats: {stats}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️  Index '{index_name}' not found in available indexes: {available_indexes}"
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Pinecone connection failed: {str(e)}")
            )
