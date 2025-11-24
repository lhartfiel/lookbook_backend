import os
from pinecone import Pinecone
from openai import OpenAI
from django.conf import settings
from .models import Style

class VectorSearchService:
    def __init__(self):
        # Initialize OpenAI
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        # Initialize Pinecone using new v3+ API
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        self.index = self.pc.Index(os.getenv('PINECONE_INDEX_NAME'))

    def generate_embedding(self, text):
        """Generate embedding for given text using OpenAI"""
        try:
            # Create embeddings — text embeddings measure the relatedness of text strings
            # Convert text to vector numbers
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def create_style_text(self, style):
        """Create searchable text from style object"""
        tags_text = ", ".join(style.tags.names()) if style.tags.exists() else ""

        text_parts = [
            style.title,
            style.description or "",
            f"Face Shape: {style.get_face_shape_display()}",
            f"Gender: {style.get_gender_display()}",
            f"Length: {style.get_length_display()}",
            f"Texture: {style.get_texture_display()}",
            f"Thickness: {style.get_thickness_display()}",
            f"Maintenance: {style.get_maintenance_display()}",
            f"Stylist: {style.stylist_name}",
            f"Tags: {tags_text}"
        ]

        return " ".join(filter(None, text_parts))

    def index_style(self, style):
        """Add or update a style in the vector database"""
        try:
            # Create searchable text
            style_text = self.create_style_text(style)

            # Generate embedding
            embedding = self.generate_embedding(style_text)
            if not embedding:
                return False

            # Prepare metadata
            metadata = {
                'style_id': style.id,
                'title': style.title,
                'description': style.description or "",
                'face_shape': style.face_shape,
                'gender': style.gender,
                'length': style.length,
                'texture': style.texture,
                'thickness': style.thickness,
                'maintenance': style.maintenance,
                'stylist_name': style.stylist_name,
                'tags': list(style.tags.names()) if style.tags.exists() else []
            }

            # Upsert to Pinecone
            self.index.upsert([(
                f"style_{style.id}",
                embedding,
                metadata
            )])

            return True

        except Exception as e:
            print(f"Error indexing style {style.id}: {e}")
            return False

    def delete_style(self, style):
        try:
            self.index.delete(ids=[f"style_{style.id}"])
        except Exception as e:
            print(f"Error deleting style {style.id}: {e}")
            return False

    def search_styles(self, query, top_k=10):
        """Search for styles based on natural language query"""
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query)
            if not query_embedding:
                return []

            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )

            # Extract style IDs and scores
            style_results = []
            print('matches', results)
            for match in results['matches']:
                style_id = match['metadata']['style_id']
                score = match['score']
                if match['score'] >= 0.75:  # Only include high-confidence matches
                    style_results.append({
                    'style_id': style_id,
                    'score': score,
                    'metadata': match['metadata']
                })

            return style_results

        except Exception as e:
            print(f"Error searching styles: {e}")
            return []

    def generate_ai_response(self, query, search_results, styles):
        """Generate AI response about the search results"""
        try:
            if not search_results:
                return "Sorry, I couldn't find any hairstyles matching your description. Try describing the look you want in different words."

            # Create context from the found styles
            styles_context = []
            for style in styles[:5]:  # Limit to top 5 for context
                tags = ", ".join(style.tags.names()) if style.tags.exists() else "No tags"
                style_info = f"- {style.title} by {style.stylist_name}: {style.description or 'No description'} (Length: {style.get_length_display()}, Texture: {style.get_texture_display()}, Maintenance: {style.get_maintenance_display()}, Tags: {tags})"
                styles_context.append(style_info)

            context_text = "\n".join(styles_context)

            prompt = f"""You are a professional hairstylist helping clients find the perfect hairstyle.

            User's request: "{query}"

            Here are the matching hairstyles I found:
            {context_text}

            Please provide a helpful, friendly response that:
            1. Acknowledges their request and references them as a trend setter, a beauty or something else stylish
            2. Briefly describes why these styles match what they're looking for
            3. Highlights 2-3 key styles that would work best
            4. Gives practical advice about maintenance, styling, or considerations
            5. Keep it conversational and encouraging
            6. Return a max of 200 words
            7. Each paragraph should be a max length of 75 words

            Response should be 1-2 paragraphs maximum."""
            response = self.openai_client.responses.create(
                model="gpt-4o-mini",
                instructions="You are a helpful hairstylist assistant.",
                input=prompt,
                max_output_tokens=250, # 1 token is approximately 4 characters or 0.75 words for English text.
                temperature=0.7
            )

            return response.output[0].content[0].text

        except Exception as e:
            print(f"Error generating AI response: {e}")
            return f"I found {len(styles)} hairstyles that match your request for '{query}'. Check out the results below!"

