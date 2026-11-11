---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 3d11ecca4deb4fbd1b1ef40a960fa73fff5217e51a1a0bbc91656e85172b2036
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: Git workflow patterns including branching strategies, commit conventions, keeping history clean and readable, tidying local commits before merging, merge vs rebase, conflict resolution, and collaborative development best practices for teams of all sizes. Use when choosing a branching strategy, writing commit conventions, cleaning up history before a pull request, deciding merge versus rebase, or resolving conflicts.
name: git-workflow
origin: ECC
---
# Git Workflow Patterns
Best practices for Git version control, branching strategies, and collaborative development.
## When to Activate
- Setting up Git workflow for a new project
- Deciding on branching strategy (GitFlow, trunk-based, GitHub flow)
- Writing commit messages and PR descriptions
- Resolving merge conflicts
- Managing releases and version tags
- Onboarding new team members to Git practices
## Branching Strategies
### GitHub Flow (Simple, Recommended for Most)
Best for continuous deployment and small-to-medium teams.
```
main (protected, always deployable)
  │
  ├── feature/user-auth      → PR → merge to main
  ├── feature/payment-flow   → PR → merge to main
  └── fix/login-bug          → PR → merge to main
```
**Rules:**
- `main` is always deployable
- Create feature branches from `main`
- Open Pull Request when ready for review
- After approval and CI passes, merge to `main`
- Deploy immediately after merge
### Trunk-Based Development (High-Velocity Teams)
Best for teams with strong CI/CD and feature flags.
```
main (trunk)
  │
  ├── short-lived feature (1-2 days max)
  ├── short-lived feature
  └── short-lived feature
```
**Rules:**
- Everyone commits to `main` or very short-lived branches
- Feature flags hide incomplete work
- CI must pass before merge
- Deploy multiple times per day
### GitFlow (Complex, Release-Cycle Driven)
Best for scheduled releases and enterprise projects.
```
main (production releases)
  │
  └── develop (integration branch)
        │
        ├── feature/user-auth
        ├── feature/payment
        │
        ├── release/1.0.0    → merge to main and develop
        │
        └── hotfix/critical  → merge to main and develop
```
**Rules:**
- `main` contains production-ready code only
- `develop` is the integration branch
- Feature branches from `develop`, merge back to `develop`
- Release branches from `develop`, merge to `main` and `develop`
- Hotfix branches from `main`, merge to both `main` and `develop`
### When to Use Which
| Strategy | Team Size | Release Cadence | Best For |
|----------|-----------|-----------------|----------|
| GitHub Flow | Any | Continuous | SaaS, web apps, startups |
| Trunk-Based | 5+ experienced | Multiple/day | High-velocity teams, feature flags |
| GitFlow | 10+ | Scheduled | Enterprise, regulated industries |
## Commit Messages
### Conventional Commits Format
```
<type>(<scope>): <subject>
[optional body]
[optional footer(s)]
```
### Types
| Type | Use For | Example |
|------|---------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): handle null response in user endpoint` |
| `docs` | Documentation | `docs(readme): update installation instructions` |
| `style` | Formatting, no code change | `style: fix indentation in login component` |
| `refactor` | Code refactoring | `refactor(db): extract connection pool to module` |
| `test` | Adding/updating tests | `test(auth): add unit tests for token validation` |
| `chore` | Maintenance tasks | `chore(deps): update dependencies` |
| `perf` | Performance improvement | `perf(query): add index to users table` |
| `ci` | CI/CD changes | `ci: add PostgreSQL service to test workflow` |
| `revert` | Revert previous commit | `revert: revert "feat(auth): add OAuth2 login"` |
### Good vs Bad Examples
```
# BAD: Vague, no context
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "WIP"
# GOOD: Clear, specific, explains why
git commit -m "fix(api): retry requests on 503 Service Unavailable
The external API occasionally returns 503 errors during peak hours.
Added exponential backoff retry logic with max 3 attempts.
Closes #123"
```
### Commit Message Template
Create `.gitmessage` in repo root:
```
# <type>(<scope>): <subject>
# # Types: feat, fix, docs, style, refactor, test, chore, perf, ci, revert
# Scope: api, ui, db, auth, etc.
# Subject: imperative mood, no period, max 50 chars
#
# [optional body] - explain why, not what
# [optional footer] - Breaking changes, closes #issue
```
Enable with: `git config commit.template .gitmessage`
## Merge vs Rebase
### Merge (Preserves History)
**Use when:**
- Merging feature branches into `main`
- You want to preserve exact history
- Multiple people worked on the branch
- The branch has been pushed and others may have based work on it
### Rebase (Linear History)
**Use when:**
- Updating your local feature branch with latest `main`
- You want a linear, clean history
- The branch is local-only (not pushed)
- You're the only one working on the branch
### Rebase Workflow
### When NOT to Rebase
```
# NEVER rebase branches that:
- Have been pushed to a shared repository
- Other people have based work on
- Are protected branches (main, develop)
- Are already merged
# Why: Rebase rewrites history, breaking others' work
```
## Pull Request Workflow
### PR Title Format
```
<type>(<scope>): <description>
Examples:
feat(auth): add SSO support for enterprise users
fix(api): resolve race condition in order processing
docs(api): add OpenAPI specification for v2 endpoints
```
### PR Description Template
### Code Review Checklist
**For Reviewers:**
- [ ] Does the code solve the stated problem?
- [ ] Are there any edge cases not handled?
- [ ] Is the code readable and maintainable?
- [ ] Are there sufficient tests?
- [ ] Are there security concerns?
- [ ] Is the commit history clean (squashed if needed)?
**For Authors:**
- [ ] Self-review completed before requesting review
- [ ] CI passes (tests, lint, typecheck)
- [ ] PR size is reasonable (<500 lines ideal)
- [ ] Related to a single feature/fix
- [ ] Description clearly explains the change
## Conflict Resolution
### Identify Conflicts
### Resolve Conflicts
### Conflict Prevention Strategies
## Branch Management
### Naming Conventions
```
# Feature branches
feature/user-authentication
feature/JIRA-123-payment-integration
# Bug fixes
fix/login-redirect-loop
fix/456-null-pointer-exception
# Hotfixes (production issues)
hotfix/critical-security-patch
hotfix/database-connection-leak
# Releases
release/1.2.0
release/2024-01-hotfix
# Experiments/POCs
experiment/new-caching-strategy
poc/graphql-migration
```
### Branch Cleanup
### Stash Workflow
## Release Management
### Semantic Versioning
```
MAJOR.MINOR.PATCH
MAJOR: Breaking changes
MINOR: New features, backward compatible
PATCH: Bug fixes, backward compatible
Examples:
1.0.0 → 1.0.1 (patch: bug fix)
1.0.1 → 1.1.0 (minor: new feature)
1.1.0 → 2.0.0 (major: breaking change)
```
### Creating Releases
### Changelog Generation
## Git Configuration
### Essential Configs
### Useful Aliases
### Gitignore Patterns
## Common Workflows
### Starting a New Feature
### Updating a PR with New Changes
### Syncing Fork with Upstream
### Undoing Mistakes
## Git Hooks
### Pre-Commit Hook
### Pre-Push Hook
## Anti-Patterns
```
# BAD: Committing directly to main
git checkout main
git commit -m "fix bug"
# GOOD: Use feature branches and PRs
# BAD: Committing secrets
git add .env  # Contains API keys
# GOOD: Add to .gitignore, use environment variables
# BAD: Giant PRs (1000+ lines)
# GOOD: Break into smaller, focused PRs
# BAD: "Update" commit messages
git commit -m "update"
git commit -m "fix"
# GOOD: Descriptive messages
git commit -m "fix(auth): resolve redirect loop after login"
# BAD: Rewriting public history
git push --force origin main
# GOOD: Use revert for public branches
git revert HEAD
# BAD: Long-lived feature branches (weeks/months)
# GOOD: Keep branches short (days), rebase frequently
# BAD: Committing generated files
git add dist/
git add node_modules/
# GOOD: Add to .gitignore
```
## Quick Reference
| Task | Command |
|------|---------|
| Create branch | `git checkout -b feature/name` |
| Switch branch | `git checkout branch-name` |
| Delete branch | `git branch -d branch-name` |
| Merge branch | `git merge branch-name` |
| Rebase branch | `git rebase main` |
| View history | `git log --oneline --graph` |
| View changes | `git diff` |
| Stage changes | `git add .` or `git add -p` |
| Commit | `git commit -m "message"` |
| Push | `git push origin branch-name` |
| Pull | `git pull origin branch-name` |
| Stash | `git stash push -m "message"` |
| Undo last commit | `git reset --soft HEAD~1` |
| Revert commit | `git revert HEAD` |