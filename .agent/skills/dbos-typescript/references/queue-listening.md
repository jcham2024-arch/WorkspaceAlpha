# Queue Listening

Scope: queue-listening (dbos-typescript).
Load when: you need the queue-listening (dbos-typescript) detail described in SKILL.md.

## Contents

- Queue Listening

## Checklist

- [ ] (see SKILL.md workflow)

## Commands

| Task | Command |
|---|---|
| see SKILL.md | — |

## Notes

- Original reference content preserved verbatim below.

--- ORIGINAL REFERENCE ---
---
title: Control Which Queues a Worker Listens To
impact: HIGH
impactDescription: Enables heterogeneous worker pools
tags: queue, listen, worker, process, configuration
---

## Control Which Queues a Worker Listens To

Configure `listenQueues` in DBOS configuration to make a process only dequeue from specific queues. This enables heterogeneous worker pools.

**Incorrect (all workers process all queues):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

// Every worker processes both CPU and GPU tasks
// GPU tasks on CPU workers will fail or be slow!
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});
await DBOS.launch();
```

**Correct (selective queue listening):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

async function main() {
  const workerType = process.env.WORKER_TYPE; // "cpu" or "gpu"

  const config: any = {
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  };

  if (workerType === "gpu") {
    config.listenQueues = [gpuQueue];
  } else if (workerType === "cpu") {
    config.listenQueues = [cpuQueue];
  } else {
    throw new Error("WORKER_TYPE must be cpu or gpu");
  }

  DBOS.setConfig(config);
  await DBOS.launch();
}
```

`listenQueues` only controls dequeuing. A CPU worker can still enqueue tasks onto the GPU queue:

```typescript
// From a CPU worker, enqueue onto the GPU queue
await DBOS.startWorkflow(gpuTask, { queueName: gpuQueue.name })("data");
```

Reference: [Explicit Queue Listening](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#explicit-queue-listening)
