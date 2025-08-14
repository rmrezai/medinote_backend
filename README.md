# MediNote Backend

Simple FastAPI service for generating patient notes.

## Running Tests

Install dependencies and execute the test suite with:

```bash
pip install -r requirements.txt
pip install pytest httpx
pytest
```

These tests cover both the core `hoop_engine` logic and the `/generate-note` API endpoint using the sample patient data.
