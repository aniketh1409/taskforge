# TaskForge Architecture (Scrappy Notes)

This is intentionally simple.
If this works, we add more features later.

## 0) Mental model

Think of it like a restaurant:

- API = cashier taking orders
- Redis queue = order line
- Worker = kitchen
- Postgres = order history board

Cashier should not cook. Kitchen should not take customer orders.

## 1) Services

### API service

- Accept job requests
- Save job row in database
- Push job id into Redis queue
- Return job id fast

### Redis

- Queue of waiting job ids
- Later: pub/sub and locks

### Worker

- Pull job id from queue
- Mark job `running`
- Execute task
- Mark job `succeeded` or `failed`

### Postgres

- Source of truth for job state
- Used by status endpoints

## 2) Data flow (MVP)

1. Client sends `POST /jobs`
2. API creates job in Postgres (`status = queued`)
3. API pushes `job_id` to Redis queue
4. Worker pops `job_id`
5. Worker updates status to `running`
6. Worker executes task
7. Worker updates job:
   - success -> `succeeded` + `result`
   - error -> `failed` + `error`
8. Client calls `GET /jobs/{id}` to check status

## 3) State machine (very important)

Allowed:

- `queued -> running`
- `running -> succeeded`
- `running -> failed`

Not allowed:

- `queued -> succeeded`
- `queued -> failed` (without running)
- `succeeded -> running`

## 4) Queue message format

Keep queue message tiny:

- `job_id`

Do not put full payload in queue for now.
Worker reads full data from Postgres using `job_id`.

## 5) First task type

Only one task type in MVP:

- `demo.sleep_echo`

Behavior:

- wait N seconds
- return a tiny result object

Reason: helps test async flow without business complexity.

## 6) Error handling (MVP)

For now:

- if worker crashes during job, job may stay `running` (we fix in later phase)
- if task throws error, mark `failed`

Later phase:

- retries
- backoff
- dead-letter

## 7) API endpoints to implement first

- `POST /jobs`
- `GET /jobs/{id}`
- `GET /jobs`

Optional later:

- `GET /health`
- WebSocket updates

## 8) Tables (initial)

### `jobs`

- id
- task_type
- payload
- status
- result
- error
- created_at
- updated_at

### `job_attempts` (next phase)

- id
- job_id
- attempt_no
- started_at
- ended_at
- error

## 9) Local run target

Use docker compose with:

- api
- worker
- redis
- postgres

Success looks like:

- submit job
- see log "queued"
- see worker log "running"
- see final status "succeeded"

## 10) Fast 3-week plan

### Week 1

- core API + queue + worker + jobs table

### Week 2

- retries + attempts + dead-letter status + multi-worker test

### Week 3

- websocket updates + deploy + basic streamlit UI

## 11) Rules to keep project fast

- Do not add new features until current phase is tested
- Keep one task type until reliability works
- Keep endpoint payloads small and stable
- Write down assumptions in docs before coding
