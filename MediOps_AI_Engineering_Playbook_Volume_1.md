# MediOps AI Engineering Playbook (Volume 1)

> This is **Volume 1** of a larger implementation guide. It contains the
> first 10 detailed phases.

# Table of Contents

1.  Project Vision
2.  System Requirements
3.  Architecture
4.  Development Standards
5.  Phase 1 -- Repository Setup
6.  Phase 2 -- Backend Foundation
7.  Phase 3 -- Frontend Foundation
8.  Phase 4 -- Docker Infrastructure
9.  Phase 5 -- PostgreSQL & Redis
10. Phase 6 -- Hospital Simulator
11. Phase 7 -- Logging
12. Phase 8 -- Authentication
13. Phase 9 -- Database Models
14. Phase 10 -- API Layer

------------------------------------------------------------------------

# Project Vision

Build a production-grade AI Operations platform for Hospital Management
Systems.

Goals:

-   Multi-agent architecture
-   RAG
-   Root Cause Analysis
-   Action Agent
-   Verification Agent
-   Incident Reporting
-   React Dashboard

------------------------------------------------------------------------

# Development Standards

Every phase must satisfy:

-   Production-quality code
-   Type hints
-   Logging
-   Error handling
-   Tests
-   Docker support
-   Environment configuration
-   Documentation

------------------------------------------------------------------------

# Universal Anti Gravity Prompt

``` text
You are a Principal AI Engineer.

Implement ONLY the requested phase.

Rules:
- Generate production-ready code.
- Never leave compile/runtime errors.
- Install dependencies.
- Run formatting.
- Run linting.
- Execute tests.
- Fix every issue automatically.
- Repeat until successful.
- Print implementation report.
```

------------------------------------------------------------------------

# Phase 1 -- Repository Setup

## Objective

Create the complete project structure.

## Deliverables

-   Monorepo
-   Backend
-   Frontend
-   Docker
-   Docs
-   Tests

## Acceptance

-   Repository builds successfully.
-   Git initialized.
-   README created.

## Anti Gravity Prompt

``` text
Create the MediOps AI repository using a clean monorepo structure.

Create:
backend/
frontend/
docs/
docker/
tests/

Initialize Git.

Create README.

Verify folder structure.

Fix every issue until complete.
```

------------------------------------------------------------------------

# Phase 2 -- Backend Foundation

Objective:

Create FastAPI backend.

Acceptance:

-   FastAPI starts.
-   /health returns HTTP 200.

Prompt:

``` text
Create a production FastAPI backend with configuration, logging, health endpoint, dependency injection, settings management and testing.

Run server.

Fix every runtime error.

Repeat until successful.
```

------------------------------------------------------------------------

# Phase 3 -- Frontend Foundation

Objective:

Create React + TypeScript application.

Acceptance:

-   Frontend compiles.
-   Landing page loads.

Prompt:

``` text
Generate React + TypeScript frontend.

Configure routing.

Create dashboard shell.

Run frontend.

Fix every compile error.
```

------------------------------------------------------------------------

# Phase 4 -- Docker Infrastructure

Prompt:

``` text
Containerize backend, frontend, PostgreSQL and Redis using Docker Compose.

Verify all services start.

Fix every issue automatically.
```

------------------------------------------------------------------------

# Phase 5 -- PostgreSQL & Redis

Prompt:

``` text
Configure PostgreSQL and Redis.

Create health checks.

Verify connectivity.

Run migrations.

Fix every issue.
```

------------------------------------------------------------------------

# Phase 6 -- Hospital Simulator

Prompt:

``` text
Implement mock services:

- Patient Portal
- Appointment
- Laboratory
- Billing
- Pharmacy
- Authentication

Generate realistic structured logs.

Verify every endpoint.
```

------------------------------------------------------------------------

# Phase 7 -- Logging

Prompt:

``` text
Implement centralized structured logging.

Support JSON logs.

Create rotating log files.

Test logging.

Fix failures.
```

------------------------------------------------------------------------

# Phase 8 -- Authentication

Prompt:

``` text
Implement JWT authentication.

Role-based access.

Refresh tokens.

Write tests.

Fix all issues.
```

------------------------------------------------------------------------

# Phase 9 -- Database Models

Prompt:

``` text
Create SQLAlchemy models for incidents, users, actions, reports, logs and knowledge base.

Generate Alembic migrations.

Run migrations.

Verify CRUD operations.
```

------------------------------------------------------------------------

# Phase 10 -- API Layer

Prompt:

``` text
Implement REST APIs for incidents, reports, users and health.

Generate OpenAPI documentation.

Run API tests.

Fix all issues.
```

------------------------------------------------------------------------

# Next Volumes

Volume 2: - RAG - Embeddings - FAISS - Knowledge Agent - Planner Agent -
Incident Intake Agent

Volume 3: - Root Cause Agent - Action Agent - Verification Agent -
LangGraph

Volume 4: - Dashboard - Monitoring - Deployment - Production Readiness
