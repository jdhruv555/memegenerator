# Automated Meme Generation & Social Media Posting System

An end-to-end system that automates meme creation and posting using LLMs and Computer Vision.

## Features

- 🔄 Daily automated meme generation pipeline
- 📊 Trending topic analysis from multiple sources
- 🤖 AI-powered caption generation using LLMs
- 🎨 Automated meme image creation
- 📱 Instagram integration for automated posting
- 📦 Scalable architecture with Celery and Redis
- 🗄️ PostgreSQL database for meme management

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL
- **AI/ML**: OpenAI GPT-4, Stable Diffusion
- **Image Processing**: Pillow, OpenCV
- **Data Sources**: NewsAPI, Google Trends, Twitter, Reddit
- **Storage**: AWS S3
- **Deployment**: Docker + GitHub Actions

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://user:password@localhost:5432/meme_db
   OPENAI_API_KEY=your_openai_key
   INSTAGRAM_ACCESS_TOKEN=your_instagram_token
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
meme_generator/
├── core/                 # Core Django app
├── memes/               # Meme generation app
├── social/              # Social media integration
├── tasks/               # Celery tasks
├── templates/           # HTML templates
├── static/             # Static files
└── manage.py           # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 