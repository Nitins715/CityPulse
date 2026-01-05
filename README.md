# 🏙️ CityPulse - Civic Infrastructure Management System

**CityPulse** is a cutting-edge, AI-powered platform designed to bridge the gap between citizens and municipal authorities. It enables real-time reporting, tracking, and resolution of civic issues like potholes, drainage problems, and street light failures.

---

## 🚀 Key Features

### 👤 For Citizens
- **Instant Reporting**: Report issues with photos and precise GPS location.
- **Auto-Detection**: Automatic address and issue type detection using AI.
- **Live Tracking**: Track the status of your reported issues in real-time.
- **Civic Map**: Visualize issues across the city on an interactive heatmap.
- **Mobile Optimized**: Fully responsive web app that works like a native mobile app.

### 🛡️ For Authorities
- **Command Center Dashboard**: Real-time overview of city infrastructure health.
- **AI Triage**: Google Gemini AI automatically classifies and prioritizes incoming reports.
- **Executive Summaries**: One-click AI generation of actionable daily reports.
- **Efficiency Tools**: Integrated maps, analytics, and team assignment workflows.

---

## 🛠️ Quick Setup Guide

### Prerequisites
- Python 3.8+
- Google Gemini API Key
- Google Maps API Key (Optional, for better location services)

### Installation

1.  **Clone & Enter Project**:
    ```bash
    cd CityPulse
    ```

2.  **Activate Virtual Environment**:
    - **Windows**: `.\venv\Scripts\activate`
    - **Mac/Linux**: `source venv/bin/activate`

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Open the `.env` file and add your API keys:
    ```env
    GEMINI_API_KEY=your_gemini_key_here
    MAPS_API_KEY=your_maps_key_here
    ```

5.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6.  **Create Admin User** (for Authority access):
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run Server**:
    ```bash
    python manage.py runserver
    ```

### Access Points
- **Citizen Portal**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Authority Dashboard**: [http://127.0.0.1:8000/authority/](http://127.0.0.1:8000/authority/) (Login with superuser credentials)

---

## 🤖 AI Capabilities (Powered by Gemini 2.0 Flash)
- **Classification**: Analyzes report descriptions to categorize issues (e.g., "Pothole" vs "Drainage").
- **Priority Scoring**: Assigns urgency levels (Low to Critical) based on context.
- **Sentiment Analysis**: Detects urgent language to flag critical safety hazards.
- **Summarization**: Generates concise status reports for city officials.

---

## 📚 Developer Resources
For detailed API endpoints, database schema, and architecture, please refer to [DEVELOPER.md](DEVELOPER.md).

---

_Built for the Hackathon 2026. Empowering Better Cities._
