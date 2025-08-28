# Fitness Tracker API

A comprehensive Django REST Framework API for tracking fitness activities, setting goals, and monitoring progress.

## Features

- **User Management**: Registration, authentication, profile management
- **Activity Tracking**: Log various types of fitness activities
- **Goals & Progress**: Set fitness goals and track progress
- **Metrics & Analytics**: View detailed activity statistics
- **Leaderboards**: Compare progress with other users
- **Advanced Filtering**: Filter activities by date, type, duration, etc.
- **JWT Authentication**: Secure token-based authentication

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL (SQLite for development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Additional**: django-cors-headers, django-filter

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd fitness_tracker_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your settings
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/token/` | Login (get tokens) |
| POST | `/api/token/refresh/` | Refresh access token |
| GET/PUT | `/api/auth/profile/` | Get/Update user profile |
| POST | `/api/auth/change-password/` | Change password |
| DELETE | `/api/auth/delete-account/` | Delete user account |

### Activities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/activities/` | List/Create activities |
| GET/PUT/DELETE | `/api/activities/{id}/` | Retrieve/Update/Delete activity |
| GET | `/api/activities/history/` | Activity history with filters |
| GET | `/api/activities/metrics/` | Activity statistics |
| GET | `/api/activities/leaderboard/` | User leaderboards |

### Goals

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/activities/goals/` | List/Create goals |
| GET/PUT/DELETE | `/api/activities/goals/{id}/` | Retrieve/Update/Delete goal |

## API Usage Examples

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

### 3. Create Activity

```bash
curl -X POST http://localhost:8000/api/activities/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "activity_type": "running",
    "duration": 30,
    "distance": 5.0,
    "calories_burned": 350,
    "date": "2024-01-15",
    "notes": "Morning run in the park"
  }'
```

### 4. Get Activity History with Filters

```bash
# Filter by date range and activity type
curl "http://localhost:8000/api/activities/history/?start_date=2024-01-01&end_date=2024-01-31&activity_type=running" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Sort by duration (descending)
curl "http://localhost:8000/api/activities/history/?ordering=-duration" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Activity Metrics

```bash
# Overall metrics
curl "http://localhost:8000/api/activities/metrics/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Metrics for specific month
curl "http://localhost:8000/api/activities/metrics/?start_date=2024-01-01&end_date=2024-01-31" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Create Fitness Goal

```bash
curl -X POST http://localhost:8000/api/activities/goals/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "goal_type": "distance",
    "target_value": 100,
    "period": "monthly",
    "activity_type": "running",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }'
```

### 7. Get Leaderboard

```bash
curl "http://localhost:8000/api/activities/leaderboard/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Filtering & Sorting Options

### Activity Filters

- `start_date`, `end_date`: Date range (YYYY-MM-DD)
- `activity_type`: Filter by activity type
- `min_duration`, `max_duration`: Duration range (minutes)
- `min_distance`, `max_distance`: Distance range (km)
- `min_calories`, `max_calories`: Calories range

### Sorting Options

- `date`: Sort by activity date
- `duration`: Sort by duration
- `distance`: Sort by distance
- `calories_burned`: Sort by calories
- Add `-` prefix for descending order (e.g., `-date`)

## Deployment

### Heroku Deployment

1. **Create Heroku App**

```bash
heroku create your-app-name
```

2. **Set Environment Variables**

```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

3. **Add PostgreSQL**

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Deploy**

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `True` |
| `DATABASE_URL` | Database connection string | SQLite |
| `ALLOWED_HOSTS` | Allowed hosts (comma-separated) | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

## Testing

Run tests with:

```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## License

This project is licensed under the MIT License.