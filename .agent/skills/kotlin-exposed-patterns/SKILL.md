---
tier: experimental
last_reviewed: 2026-11-10
content_hash: 0530471593308ab1c386a5dc8af6cedc0daedd85b5f3e0be8c7fd3d51741474e
fetched_at: 2026-11-10
upstream_license: unknown
owner: taskmaster
description: JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP connection pooling, Flyway migrations, and repository pattern. Use when working with the Exposed ORM — DSL or DAO queries, transactions, pooling, or migrations.
name: kotlin-exposed-patterns
origin: ECC
---
# Kotlin Exposed Patterns
Comprehensive patterns for database access with JetBrains Exposed ORM, including DSL queries, DAO, transactions, and production-ready configuration.
## When to Use
- Setting up database access with Exposed
- Writing SQL queries using Exposed DSL or DAO
- Configuring connection pooling with HikariCP
- Creating database migrations with Flyway
- Implementing the repository pattern with Exposed
- Handling JSON columns and complex queries
## How It Works
Exposed provides two query styles: DSL for direct SQL-like expressions and DAO for entity lifecycle management. HikariCP manages a pool of reusable database connections configured via `HikariConfig`. Flyway runs versioned SQL migration scripts at startup to keep the schema in sync. All database operations run inside `newSuspendedTransaction` blocks for coroutine safety and atomicity. The repository pattern wraps Exposed queries behind an interface so business logic stays decoupled from the data layer and tests can use an in-memory H2 database.
## Examples
### DSL Query
### DAO Entity Usage
### HikariCP Configuration
## Database Setup
### HikariCP Connection Pooling
### Flyway Migrations
### Migration Files
## Table Definitions
### DSL Style Tables
### Composite Tables
## DSL Queries
### Basic CRUD
### Advanced Queries
### Pagination
### Batch Operations
## DAO Pattern
### Entity Definitions
### DAO Operations
## Transactions
### Suspend Transaction Support
### Transaction Isolation
## Repository Pattern
### Interface Definition
### Exposed Implementation
## JSON Columns
### JSONB with kotlinx.serialization
## Testing with Exposed
### In-Memory Database for Tests
## Gradle Dependencies
## Quick Reference: Exposed Patterns
| Pattern | Description |
|---------|-------------|
| `object Table : UUIDTable("name")` | Define table with UUID primary key |
| `newSuspendedTransaction { }` | Coroutine-safe transaction block |
| `Table.selectAll().where { }` | Query with conditions |
| `Table.insertAndGetId { }` | Insert and return generated ID |
| `Table.update({ condition }) { }` | Update matching rows |
| `Table.deleteWhere { }` | Delete matching rows |
| `Table.batchInsert(items) { }` | Efficient bulk insert |
| `innerJoin` / `leftJoin` | Join tables |
| `orderBy` / `limit` / `offset` | Sort and paginate |
| `count()` / `sum()` / `avg()` | Aggregation functions |
**Remember**: Use the DSL style for simple queries and the DAO style when you need entity lifecycle management. Always use `newSuspendedTransaction` for coroutine support, and wrap database operations behind a repository interface for testability.
## Platform variants
OS-specific companions for this skill:
- [Android](platforms/android.md)