# Reference

Scope: moved detail from SKILL.md.
Load when: needed by the operation described in SKILL.md.

## Contents

- Reference

## Checklist

- [ ] (see SKILL.md)

## Commands

| Fallback | Command |
|---|---|
| see body | — |

## Notes

- Original code preserved verbatim from SKILL.md.

```
```csharp
// Common system event types
using Azure.Messaging.EventGrid.SystemEvents;

// Storage events
StorageBlobCreatedEventData blobCreated;
StorageBlobDeletedEventData blobDeleted;

// Resource events
ResourceWriteSuccessEventData resourceCreated;
ResourceDeleteSuccessEventData resourceDeleted;

// App Service events
WebAppUpdatedEventData webAppUpdated;

// Container Registry events
ContainerRegistryImagePushedEventData imagePushed;

// IoT Hub events
IotHubDeviceCreatedEventData deviceCreated;
```

```
