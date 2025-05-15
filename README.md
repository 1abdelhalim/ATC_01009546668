# Event Booking System

A full-stack event booking system built with Django, featuring a modern UI with Tailwind CSS and HTMX.

## 🌟 Features

### Public Features
- Browse and search events
- Book events with instant confirmation
- User authentication (login/register)
- Dark mode support
- Responsive design for all devices
- Multi-language support (English + Arabic)

### Admin Features
- Custom admin dashboard
- CRUD operations for events
- Booking management
- User management
- Real-time updates with HTMX

## 🛠 Tech Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Frontend**: Django Templates + HTMX + Tailwind CSS
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Deployment**: Docker + Azure Web App
- **CI/CD**: GitHub Actions
- **Authentication**: Django Auth System
- **API Documentation**: Swagger/ReDoc

## 🚀 Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/event-booking-system.git
cd event-booking-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t event-booking-system .
```

2. Run the container:
```bash
docker run -p 8000:8000 event-booking-system
```

## 📦 Project Structure

```
event_booking/
├── core/               # Core app for shared components
├── users/             # User authentication and management
├── events/            # Event management
├── bookings/          # Booking management
├── static/            # Static files
├── templates/         # HTML templates
├── media/             # User-uploaded files
└── manage.py          # Django management script
```

## 🔒 Security Features

- CSRF protection
- Role-based access control
- Secure file uploads
- Environment variable management
- Production security settings

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📚 API Documentation

API documentation is available at:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎨 UI Preview

[Add screenshots here after deployment]

## 🛠️ Built with AI Tools

This project was built with assistance from:
- Cursor AI: Code generation and refactoring
- GitHub Copilot: Code suggestions and completions
- ChatGPT: Architecture planning and documentation

## 🔗 Links

- [Live Demo](https://your-demo-url.com)
- [API Documentation](https://your-demo-url.com/api/docs/)