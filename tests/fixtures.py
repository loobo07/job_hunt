ADZUNA_RAW_JOB = {
    "id": "adz-1",
    "title": "Senior Python Backend Engineer",
    "company": {"display_name": "Acme Data"},
    "location": {"display_name": "New York, NY", "area": ["US", "New York"]},
    "description": "Build FastAPI services with Python, SQL, and data pipelines.",
    "redirect_url": "https://example.com/adzuna/acme-python",
    "created": "2026-06-20T12:00:00Z",
    "salary_min": 150000,
    "salary_max": 190000,
    "contract_type": "permanent",
    "contract_time": "full_time",
    "category": {"tag": "it-jobs"},
    "salary_is_predicted": False,
}

GREENHOUSE_RAW_JOB = {
    "id": 2001,
    "internal_job_id": 901,
    "title": "Backend Platform Engineer",
    "content": "Own Python APIs, PostgreSQL data models, and reliable job workflows.",
    "department": "Engineering",
    "office": {"name": "Remote - United States"},
    "metadata": [{"name": "Workplace Type", "value": "Remote"}],
    "absolute_url": "https://boards.greenhouse.io/acme/jobs/2001",
}

SAMPLE_PROFILE = {
    "target_titles": ["Backend Engineer", "Platform Engineer"],
    "must_have_skills": ["python", "fastapi"],
    "nice_to_have_skills": ["postgresql", "sqlalchemy"],
    "years_experience": 6,
    "locations": ["New York, NY", "Remote - United States"],
    "remote_preference": "remote",
    "salary_min": 140000,
    "excluded_companies": ["BadCo"],
    "excluded_keywords": ["frontend-only"],
}
