# MediNote Backend

FastAPI backend for generating clinical notes.

## Installation

```bash
git clone https://github.com/<your-org>/medinote_backend.git
cd medinote_backend
pip install -r requirements.txt
```

## Running the Server

Launch the FastAPI app with Uvicorn:

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to confirm the API is up.

### Example Request

```bash
curl -X POST "http://localhost:8000/generate-note" \
  -H "Content-Type: application/json" \
  -d '{"POC_glucose": [], "active_meds": []}'
```

## Deployment

The repository includes a `render.yaml` manifest and accompanying `render-build.sh`
script for deploying on [Render](https://render.com). The build script installs
prebuilt wheels and the service runs with the start command defined in
`render.yaml`.

## Future Roadmap

- Integrate a database for persistent storage
- Add authentication and user management
- Expand test coverage and CI/CD

## Testing

Run the test suite with:

```bash
pytest
```
