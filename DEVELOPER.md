# 🧑‍💻 CityPulse Developer Documentation

This document outlines the API endpoints and technical architecture of the CityPulse system.

## 🔌 API Reference - User (Citizen)

Base URL: `/api/user/`

### Issues
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/issues/` | Submit a new civic issue. Requires `multipart/form-data` for images. |
| `GET` | `/issues/` | List all issues submitted by the authenticated user. |
| `GET` | `/issues/{id}/` | Get details of a specific issue. |
| `GET` | `/issues/map_data/` | Get lightweight data for all issues (for map visualization). |
| `GET` | `/issues/nearby/` | Get issues near a specific lat/long radius. |

**Submit Issue Payload:**
```json
{
  "title": "Broken Streetlight",
  "description": "Light poll #43 is flickering dangerously.",
  "latitude": "28.4595",
  "longitude": "77.0266",
  "address": "Sector 56, Gurugram",
  "issue_type": "STREETLIGHT",
  "image": "(Binary File)"
}
```

---

## 🔌 API Reference - Authority (Admin)

Base URL: `/api/authority/`

### Dashboard & Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dashboard/overview/` | Get aggregate stats (Total, Pending, Critical, etc.). |
| `GET` | `/dashboard/generate_report/` | Trigger AI generation of an executive summary report. |
| `GET` | `/analytics/` | Get time-series data for analysis (Daily trends, priority distribution). |

### Issue Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/issues/` | List all issues with advanced filtering (status, area, priority). |
| `PATCH` | `/issues/{id}/update_status/` | Update status, priority, or assign staff. |
| `POST` | `/issues/{id}/add_comment/` | Add an official administrative comment. |
| `DELETE` | `/user/issues/{id}/` | **Danger**: Permanently delete an issue record. |

---

## 🏗️ Architecture

### Tech Stack
- **Backend**: Django & Django REST Framework (DRF)
- **Database**: SQLite (Dev) / PostgreSQL (Prod ready)
- **AI Engine**: Google Gemini 2.0 Flash (via `google-generativeai`)
- **Maps**: Google Maps Platform (Reverse Geocoding) & Leaflet.js (Frontend Vis)

### AI Integration (`gemini_service.py`)
The system uses a custom service wrapper around the Gemini API to:
1.  **Ingest** raw issue descriptions.
2.  **Prompt** the model to classify into standard categories (Road, Water, etc.).
3.  **Evaluate** urgency to assign priority scores.
4.  **Parse** the structured JSON response back into the Django model.

### Authentication
- Session-based authentication is used for the web frontend.
- CSRF protection is enforced for all POST/PUT/DELETE requests.
- `IsStaff` permission class protects all `/authority/` endpoints.

---

## 🧪 Testing

To run the test suite:
```bash
python manage.py test
```

To verify the AI connection:
Run the `debug_models_file.py` script (if available) or check the server logs during issue submission.
