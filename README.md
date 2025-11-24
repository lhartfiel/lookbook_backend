# Lookbook Backend

Django REST API backend for the RAG Hair Lookbook application with AI-powered vector search.

## Features

- 🔍 **Vector Search**: Semantic search using Pinecone and OpenAI embeddings
- 🤖 **AI Responses**: GPT-powered conversational responses about search results
- 📸 **Image Management**: Upload and serve hairstyle images with multiple angles
- 🏷️ **Tagging System**: Flexible tagging with django-taggit
- 🔐 **REST API**: Full CRUD operations with Django REST Framework
- ❤️ **Favorites**: Retrieve favorited styles by ID

## Tech Stack

- **Framework**: Django 4.0+
- **API**: Django REST Framework
- **Database**: SQLite (dev) / MySQL (production)
- **Vector DB**: Pinecone
- **AI**: OpenAI (embeddings & chat)
- **Tags**: django-taggit
- **CORS**: django-cors-headers

## Getting Started

### Prerequisites

- Python 3.9 or higher (3.10 recommended)
- pip
- Virtual environment tool (venv, virtualenv, or conda)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd lookbook_backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy environment variables:

```bash
cp .env.example .env
```

5. Update `.env` with your configuration values (see Environment Variables section)

6. Run migrations:

```bash
python manage.py migrate
```

7. Create a superuser (optional but recommended):

```bash
python manage.py createsuperuser
```

8. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (Development uses SQLite by default)
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000

# AI and Vector Search
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_ENVIRONMENT=us-east-1-aws
PINECONE_INDEX_NAME=hair-styles
OPENAI_API_KEY=your-openai-api-key
```

### Required API Keys

1. **Pinecone**: Sign up at [pinecone.io](https://www.pinecone.io/)

   - Create a new index named `hair-styles`
   - Dimension: 1536 (for OpenAI text-embedding-3-small)
   - Metric: cosine

2. **OpenAI**: Get API key from [platform.openai.com](https://platform.openai.com/)

## Project Structure

```
lookbook_backend/
├── styles/                           # Main Django app
│   ├── management/                   # Custom management commands
│   │   └── commands/
│   │       ├── index_styles.py       # Index styles in Pinecone
│   │       └── test_connections.py   # Test API connections
│   ├── migrations/                   # Database migrations
│   ├── models.py                     # Style and Image models
│   ├── views.py                      # API endpoints
│   ├── serializers.py                # DRF serializers
│   ├── vector_search.py              # Pinecone & OpenAI integration
│   ├── urls.py                       # App URL routing
│   ├── admin.py                      # Django admin configuration
│   ├── apps.py                       # App configuration
│   ├── signals.py                    # Django signals
│   └── tests.py                      # Unit tests
├── lookbook_backend/                 # Project settings
│   ├── settings.py                   # Django settings
│   ├── urls.py                       # Main URL routing
│   ├── wsgi.py                       # WSGI configuration
│   ├── asgi.py                       # ASGI configuration
│   └── __init__.py
├── media/                            # User uploaded files
│   └── styles/                       # Hairstyle images
├── venv/                             # Virtual environment (not in git)
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
├── db.sqlite3                        # SQLite database (development)
├── .env                              # Environment variables (not in git)
├── .env.example                      # Environment template
├── .gitignore                        # Git ignore rules
├── test_pinecone_standalone.py       # Standalone Pinecone test
└── README.md                         # This file
```

## API Endpoints

### Search

- `POST /api/search/` - Natural language search for hairstyles
  ```json
  {
    "query": "short curly hair for round face"
  }
  ```

### Styles

- `GET /api/styles/` - List all styles
- `GET /api/styles/{id}/` - Get style details
- `POST /api/styles/` - Create new style (admin)
- `PUT /api/styles/{id}/` - Update style (admin)
- `DELETE /api/styles/{id}/` - Delete style (admin)

### Favorites

- `GET /api/favorites/?ids=1,2,3` - Get multiple styles by IDs

## Deployment to PythonAnywhere

### Prerequisites

- PythonAnywhere account (free or paid)
- Git repository with your code

### Deployment Steps

1. **Create a PythonAnywhere Account**

   - Sign up at [pythonanywhere.com](https://www.pythonanywhere.com/)

2. **Clone Your Repository**

   ```bash
   cd ~
   git clone <your-repo-url>
   cd lookbook_backend
   ```

3. **Create Virtual Environment**

   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 lookbook-env
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   - Create `.env` file in project root
   - Add all required environment variables
   - Set `DEBUG=False`
   - Set `ALLOWED_HOSTS=your-username.pythonanywhere.com`

5. **Configure Web App**

   - Go to Web tab in PythonAnywhere dashboard
   - Add a new web app (Python 3.10)
   - Choose "Manual configuration"
   - Set source code directory: `/home/username/lookbook_backend`
   - Set working directory: `/home/username/lookbook_backend`

6. **Configure WSGI File**
   Edit the WSGI configuration file:

   ```python
   import os
   import sys
   from dotenv import load_dotenv

   path = '/home/username/lookbook_backend'
   if path not in sys.path:
       sys.path.append(path)

   # Load environment variables
   load_dotenv(os.path.join(path, '.env'))

   os.environ['DJANGO_SETTINGS_MODULE'] = 'lookbook_backend.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

7. **Configure Static Files**
   In the Web tab, add static files mapping:

   - URL: `/media/`
   - Directory: `/home/username/lookbook_backend/media/`

8. **Run Migrations**

   ```bash
   cd ~/lookbook_backend
   workon lookbook-env
   python manage.py migrate
   python manage.py createsuperuser
   ```

9. **Reload Web App**
   - Click "Reload" button in Web tab

### Post-Deployment

1. **Test the API**

   - Visit `https://your-username.pythonanywhere.com/api/`
   - Test search endpoint
   - Verify images load correctly

2. **Update Frontend**

   - Set `NEXT_PUBLIC_API_URL` to your PythonAnywhere URL
   - Redeploy frontend

3. **Index Existing Styles**
   If you have existing styles, index them in Pinecone:

   ```python
   python manage.py shell
   from styles.models import Style
   from styles.vector_search import VectorSearchService

   service = VectorSearchService()
   for style in Style.objects.all():
       service.index_style(style)
   ```

## Database Configuration

### Development (SQLite)

Default configuration - no additional setup required.

### Production (MySQL)

1. Uncomment `mysqlclient` in `requirements.txt`
2. Install MySQL client:
   ```bash
   pip install mysqlclient
   ```
3. Update `.env`:
   ```env
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=your_database_host
   DB_PORT=3306
   ```

## Vector Search

The application uses Pinecone for vector similarity search:

1. **Indexing**: When a style is created/updated, it's automatically indexed in Pinecone
2. **Search**: User queries are converted to embeddings and matched against indexed styles
3. **Fallback**: If vector search fails, falls back to text-based search

### Manual Indexing

To manually index a style:

```python
from styles.models import Style
from styles.vector_search import VectorSearchService

service = VectorSearchService()
style = Style.objects.get(id=1)
service.index_style(style)
```

## Admin Interface

Access the Django admin at `/admin/`:

- Manage styles and images
- Add/edit tags
- View all data

## Troubleshooting

### Images not loading

- Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- Verify static files mapping in PythonAnywhere
- Ensure files have correct permissions

### CORS errors

- Add frontend domain to `CORS_ALLOWED_ORIGINS`
- Restart web app after changes

### Vector search not working

- Verify Pinecone API key and index name
- Check OpenAI API key
- Ensure styles are indexed in Pinecone

### 500 errors

- Check error logs in PythonAnywhere
- Verify all environment variables are set
- Check database connection

## Development Tips

- Use `DEBUG=True` for development
- Run `python manage.py check` to verify configuration
- Use Django shell for testing: `python manage.py shell`
- Monitor API requests in browser DevTools

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

[Your License Here]

## Support

For issues or questions, please open an issue in the repository.
