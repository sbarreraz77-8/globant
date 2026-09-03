### Purpose

The `.github` directory contains automation configurations for Continuous Integration and Continuous Deployment (CI/CD) targeting Google Cloud Platform (GCP), as well as automated testing pipelines.

---

## Workflow: globant_GCP_API

### Triggers
- **Push to branch:** `main`
- **Manual dispatch:** `workflow_dispatch` (enables on-demand execution via GitHub UI).

---

### Environment Variables
- `REGION`: Target Google Cloud deployment region (`us-central1`).
- `REPO_NAME`: Artifact Registry Docker repository name (`globant-repo`).
- `SERVICE_NAME`: Cloud Run service identifier (`globant-api`).

---

### Secret Dependencies
- `GCP_PROJECT_ID`: Target GCP project identifier.
- `GCP_CREDENTIALS`: Service account private key JSON payload.
- `DATABASE_URL`: Production PostgreSQL connection string injected into Cloud Run runtime environment.

---

### Pipeline Execution Stages
1. **Source Checkout:** Clones the repository using `actions/checkout@v4`.
2. **GCP Authentication:** Authenticates against Google Cloud using `google-github-actions/auth@v2`.
3. **Artifact Registry Provisioning:** Validates if `globant-repo` exists; creates a standard Docker format repository if absent.
4. **Docker Build & Push:** Compiles the container image tagged with the commit SHA (`${{ github.sha }}`) and pushes to Artifact Registry.
5. **Cloud Run Deployment:** Deploys the container to Cloud Run with 512Mi memory, 1 vCPU, public access enabled (`--allow-unauthenticated`), and runtime database credentials injection.

---

## Workflow: globant_run_tests

### Triggers
- **Push to branch:** `main` (Filtered by paths: `app/**`, `tests/**`, `requirements.txt`).
- **Pull Request:** `main` (Filtered by paths: `app/**`, `tests/**`, `requirements.txt`).
- **Manual dispatch:** `workflow_dispatch`.

---

### Pipeline Execution Stages
1. **Source Checkout:** Clones the repository using `actions/checkout@v4`.
2. **Python Setup:** Provisions a Python 3.11 environment with `pip` caching enabled via `actions/setup-python@v5`.
3. **Dependencies Installation:** Upgrades pip and installs project requirements from `requirements.txt`.
4. **Test Execution:** Runs the `pytest -v` test suite to validate API logic and data validation schemas.

---