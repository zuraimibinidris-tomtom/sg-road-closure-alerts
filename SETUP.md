# Development Setup Guide

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 12 or higher
- Redis 6 or higher
- Docker & Docker Compose (optional)

## Quick Start (Local)

### 1. Clone the Repository
```bash
git clone https://github.com/zuraimibinidris-tomtom/sg-road-closure-alerts.git
cd sg-road-closure-alerts
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
```bash
cp .env.example .env
# Edit .env with your local configuration
```

### 5. Create Database
```bash
# Make sure PostgreSQL is running
psql -U postgres -c "CREATE DATABASE road_closures_dev;"
```

### 6. Run Application
```bash
python app/main.py
```

The app will be available at `http://localhost:5000`

## Quick Start (Docker)

### 1. Build and Run
```bash
docker-compose up --build
```

This will start:
- Flask app on http://localhost:5000
- PostgreSQL database
- Redis cache

### 2. Stop Services
```bash
docker-compose down
```

## Testing

Run tests with pytest:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app tests/
```

## LTA API Integration

To enable real-time road closure monitoring:

1. Register at [MyTransport Data Mall](https://datamall.lta.gov.sg/)
2. Get your API key and Account Key
3. Add to `.env`:
   ```
   LTA_API_KEY=your_api_key
   LTA_ACCOUNT_KEY=your_account_key
   ```

## API Endpoints

### Health Check
- `GET /api/health` - Server health status

### Road Closures
- `GET /api/closures` - Get all closures
- `GET /api/closures?status=active` - Get closures by status
- `GET /api/closures/<id>` - Get closure details
- `POST /api/closures` - Create closure

### User Alerts
- `POST /api/alerts` - Subscribe to alerts
- `GET /api/alerts/user/<user_id>` - Get user's alerts
- `DELETE /api/alerts/<alert_id>` - Unsubscribe

## Database Schema

### users
- id, email, phone, name, created_at, updated_at

### road_closures
- id, external_id, road_name, description, status, severity, latitude, longitude, start_time, end_time, created_at, updated_at

### user_alerts
- id, user_id, area_name, latitude, longitude, radius_km, enable_sms, enable_email, enable_push, is_active, created_at, updated_at

## Next Steps

1. **Frontend Integration**: Connect to this backend from your frontend app
2. **Authentication**: Add JWT or OAuth2 authentication
3. **Real-time Updates**: Setup WebSockets for live closure updates
4. **Notifications**: Implement SMS/Email/Push notifications
5. **Task Scheduling**: Setup Celery for periodic LTA API polling
