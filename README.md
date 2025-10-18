# Lookbook Backend

Django REST API backend for the RAG Hair Lookbook application.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

3. Update `.env` with your configuration values.

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser (optional):

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: Database configuration
- `PINECONE_API_KEY`: Pinecone vector database API key
- `OPENAI_API_KEY`: OpenAI API key for embeddings
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

## Database Configuration

- **Development**: Uses SQLite (no additional setup required)
- **Production**: Uses MySQL (requires mysqlclient package and MySQL server)

## Project Structure

```
lookbook_backend/
├── apps/                   # Django applications
├── lookbook_backend/       # Main project settings
├── media/                  # User uploaded files
├── staticfiles/           # Collected static files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```
