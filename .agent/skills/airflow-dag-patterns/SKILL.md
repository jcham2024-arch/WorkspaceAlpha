---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 5bb557e588c201f171b2e8946841444c402f3ea42089919a3cd5333fa33e747b
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
date_added: 2026-02-27
description: Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs.
name: airflow-dag-patterns
risk: safe
source: community
---
# Apache Airflow DAG Patterns
Production-ready patterns for Apache Airflow including DAG design, operators, sensors, testing, and deployment strategies.
## Use this skill when
- Creating data pipeline orchestration with Airflow
- Designing DAG structures and dependencies
- Implementing custom operators and sensors
- Testing Airflow DAGs locally
- Setting up Airflow in production
- Debugging failed DAG runs
## Do not use this skill when
- You only need a simple cron job or shell script
- Airflow is not part of the tooling stack
- The task is unrelated to workflow orchestration
## Instructions
1. Identify data sources, schedules, and dependencies.
2. Design idempotent tasks with clear ownership and retries.
3. Implement DAGs with observability and alerting hooks.
4. Validate in staging and document operational runbooks.
Refer to `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.
## Safety
- Avoid changing production DAG schedules without approval.
- Test backfills and retries carefully to prevent data duplication.
## Resources
- `resources/implementation-playbook.md` for detailed patterns, checklists, and templates.
## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.