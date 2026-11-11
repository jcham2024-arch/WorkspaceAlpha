---
name: azure-eventgrid-dotnet
description: Azure Event Grid SDK for .NET. Client library for publishing and consuming events with Azure Event Grid. Use for event-driven architectures, pub/sub messaging, CloudEvents, and EventGridEvents.
risk: critical
source: community
date_added: '2026-02-27'
---
# Azure.Messaging.EventGrid (.NET)
Client library for publishing events to Azure Event Grid topics, domains, and namespaces.
## Installation

**Historical example version**: 4.28.0; verify and pin compatible SDK/Functions packages.

## Environment Variables


## Client Hierarchy

```
Push Delivery (Topics/Domains)
└── EventGridPublisherClient
    ├── SendEventAsync(EventGridEvent)
    ├── SendEventsAsync(IEnumerable<EventGridEvent>)
    ├── SendEventAsync(CloudEvent)
    └── SendEventsAsync(IEnumerable<CloudEvent>)

Pull Delivery (Namespaces)
├── EventGridSenderClient
│   └── SendAsync(CloudEvent)
└── EventGridReceiverClient
    ├── ReceiveAsync()
    ├── AcknowledgeAsync()
    ├── ReleaseAsync()
    └── RejectAsync()
```

## Authentication

### API Key Authentication


### Microsoft Entra ID (Recommended)


### SAS Token Authentication


## Publishing Events

### EventGridEvent Schema


### CloudEvent Schema


### Publishing to Event Grid Domain


### Custom Serialization


## Pull Delivery (Namespaces)

### Send Events to Namespace Topic


### Receive and Process Events


### Reject Events (dead-letter behavior depends on subscription configuration)


## Consuming Events (Azure Functions)

### EventGridEvent Trigger


### CloudEvent Trigger


## Parsing Events

### Parse EventGridEvent


### Parse CloudEvent


## System Events


## Key Types Reference

| Type | Purpose |
|------|---------|
| `EventGridPublisherClient` | Publish to topics/domains |
| `EventGridSenderClient` | Send to namespace topics |
| `EventGridReceiverClient` | Receive from namespace subscriptions |
| `EventGridEvent` | Event Grid native schema |
| `CloudEvent` | CloudEvents 1.0 schema |
| `ReceiveResult` | Pull delivery response |
| `ReceiveDetails` | Event with broker properties |
| `BrokerProperties` | Lock token, delivery count |

## Event Schemas Comparison

| Feature | EventGridEvent | CloudEvent |
|---------|----------------|------------|
| Standard | Azure-specific | CNCF standard |
| Required fields | Verify the selected Event Grid schema | specversion, id, source, type (SDK may initialize some) |
| Extensibility | Limited | Extension attributes |
| Interoperability | Azure only | Cross-platform |

## Best Practices

1. **Use CloudEvents** — Prefer CloudEvents for new implementations (industry standard)
2. **Batch events** — Send multiple events in one call for efficiency
3. **Use Entra ID** — Prefer managed identity over access keys
4. **Idempotent handlers** — Events may be delivered more than once
5. **Set event TTL** — Configure time-to-live for namespace events
6. **Handle partial failures** — Acknowledge/release events individually
7. **Use dead-letter** — Configure dead-letter for failed events
8. **Validate schemas** — Validate event data before processing

## Error Handling


## Failover Pattern


## Related SDKs

| SDK | Purpose | Install |
|-----|---------|---------|
| `Azure.Messaging.EventGrid` | Topics/Domains (this SDK) | `dotnet add package Azure.Messaging.EventGrid` |
| `Azure.Messaging.EventGrid.Namespaces` | Pull delivery | `dotnet add package Azure.Messaging.EventGrid.Namespaces` |
| `Azure.Identity` | Authentication | `dotnet add package Azure.Identity` |
| `Microsoft.Azure.WebJobs.Extensions.EventGrid` | Azure Functions trigger | `dotnet add package Microsoft.Azure.WebJobs.Extensions.EventGrid` |

## Reference Links

| Resource | URL |
|----------|-----|
| NuGet Package | https://www.nuget.org/packages/Azure.Messaging.EventGrid |
| API Reference | https://learn.microsoft.com/dotnet/api/azure.messaging.eventgrid |
| Quickstart | https://learn.microsoft.com/azure/event-grid/custom-event-quickstart |
| Pull Delivery | https://learn.microsoft.com/azure/event-grid/pull-delivery-overview |
| GitHub Source | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/eventgrid/Azure.Messaging.EventGrid |

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.

Snippets are separate fragments, not a compiled application. Use the actual topic input schema, endpoint and subscription mode; do not mix Functions in-process and isolated-worker imports/packages. Protect event payloads and SAS/lock tokens from logs. Verify per-event acknowledgement failures and lock expiry; reject can discard events when dead-lettering is not configured. Cross-region publishing may duplicate accepted events and does not transfer subscriptions or guarantee ordering; retain stable event IDs and deduplicate durably. Validate webhook authentication/subscription challenges and schemas before processing. Limits vary by topic/namespace API and must be verified.

## Platform variants

OS-specific companions for this skill:

- [Windows](platforms/windows.md)
