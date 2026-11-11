# Master Skill Categorization (rule-based)

Task types and subtypes for all 3,520 master skills (auto-classified from name + description; re-run .agent/tools/categorize.py to regenerate).

## Task-type tally

- design-ui: 854
- data-ai: 441
- project-mgmt: 413
- backend-systems: 413
- writing-content: 337
- general: 305
- frontend-web: 215
- media-video: 151
- devops-infra: 111
- automation: 68
- testing-debug: 66
- security: 47
- research: 46
- business: 37
- docs: 16

## Subtypes (top 25)

- design-ui/design-ui: 664
- data-ai/data-ai: 431
- project-mgmt/project-mgmt: 346
- general/general: 305
- writing-content/writing-content: 248
- backend-systems/backend-systems: 238
- frontend-web/frontend-web: 111
- backend-systems/api-design: 106
- design-ui/api-design: 83
- automation/automation: 68
- testing-debug/testing-debug: 66
- media-video/media-video: 64
- media-video/video: 60
- devops-infra/devops-infra: 59
- devops-infra/devops: 50
- research/research: 46
- design-ui/devops: 37
- business/business: 37
- security/security: 36
- backend-systems/python: 34
- writing-content/story-script: 32
- frontend-web/api-design: 31
- frontend-web/html: 25
- frontend-web/javascript: 22
- project-mgmt/api-design: 21

## Levels

- manager: 1374
- worker: 2146

## Per-agent scoping

Profiles provision by category + level, not whole library:
- conceptualizer: project-mgmt/worker + writing-content/worker (scope)
- taskmaster: project-mgmt/manager + automation/worker (dispatch)
- coding-manager: backend-systems + frontend-web / worker (steps)
- research-manager: research / worker (steps)
- review-manager: testing-debug + security / manager (checks)
