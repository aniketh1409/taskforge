# TaskForge (MVP)

Simple goal: submit a job, process it in background, track status.

This repo is for learning distributed backend basics without overbuilding.

## What we are building first

- API service (FastAPI): receives job requests
- Redis queue: holds waiting jobs
- Worker service: pulls jobs and executes them
- Postgres: stores job state

## MVP scope (frozen)

- One job type only
- One queue only
- Status flow only: `queued -> running -> succeeded | failed`
- No priority queue
- No delayed jobs
- No cancellation
- No auth

## Why this exists

Synchronous requests are bad for long tasks.  
TaskForge makes long work asynchronous so API stays fast.

## Core flow

1. Client calls `POST /jobs`
2. API writes job to Postgres with status `queued`
3. API pushes job id to Redis queue
4. Worker pops job id from queue
5. Worker marks job `running`, does task
6. Worker marks job `succeeded` or `failed`
7. Client checks with `GET /jobs/{id}`

## API (MVP contract)

### `POST /jobs`

Request:

- `task_type` (string, for now always one value)
- `payload` (object)
- `idempotency_key` (string, optional in MVP v1, required later)

Response:

- `job_id` (uuid)
- `status` (`queued`)
- `created_at` (timestamp)

### `GET /jobs/{id}`

Response:

- `job_id`
- `status`
- `payload`
- `result` (nullable)
- `error` (nullable)
- `created_at`
- `updated_at`

### `GET /jobs`

Response: list of jobs (latest first, basic pagination later)

## Database (MVP contract)

### `jobs`

- `id` (uuid, pk)
- `task_type` (text)
- `payload` (jsonb)
- `status` (text)
- `result` (jsonb, nullable)
- `error` (text, nullable)
- `created_at` (timestamp)
- `updated_at` (timestamp)

### `job_attempts` (Phase 2+)

- `id` (uuid, pk)
- `job_id` (uuid, fk -> jobs.id)
- `attempt_no` (int)
- `started_at` (timestamp)
- `ended_at` (timestamp, nullable)
- `error` (text, nullable)

## Status transition rules

- `queued -> running`
- `running -> succeeded`
- `running -> failed`
- No direct `queued -> succeeded`
- No direct `failed -> running` in MVP (retry comes next phase)

## Definition of done for current phase

- Can submit a job and receive `job_id`
- Worker can process queued job
- Can fetch job status by id
- Logs show the full path: submit -> queue -> start -> finish
