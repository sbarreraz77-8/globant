
### Purpose

The `.github` directory contains automation configurations for Continuous Integration and Continuous Deployment (CI/CD) targeting Google Cloud Platform (GCP).

---

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
- `GCP_CREDENTIALS`: Service account private key JSON payload
- `DATABASE_URL`: Production PostgreSQL connection string injected into Cloud Run runtime environment.

---

### Pipeline Execution Stages
1. **Source Checkout:** Clones the repository using `actions/checkout@v4`.
2. **GCP Authentication:** Authenticates against Google Cloud using `google-github-actions/auth@v2`.
3. **Artifact Registry Provisioning:** Validates if `globant-repo` exists; creates a standard Docker format repository if absent.
4. **Docker Build & Push:** Compiles the container image tagged with the commit SHA (`${{ github.sha }}`) and pushes to Artifact Registry.
5. **Cloud Run Deployment:** Deploys the container to Cloud Run with 512Mi memory, 1 vCPU, public access enabled (`--allow-unauthenticated`), and runtime database credentials injection.

---
