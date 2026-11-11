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
```kotlin
// Join queries
suspend fun findOrdersWithUser(userId: UUID): List<OrderWithUser> =
    newSuspendedTransaction {
        (OrdersTable innerJoin UsersTable)
            .selectAll()
            .where { OrdersTable.userId eq userId }
            .orderBy(OrdersTable.createdAt, SortOrder.DESC)
            .map { row ->
                OrderWithUser(
                    orderId = row[OrdersTable.id].value,
                    status = row[OrdersTable.status],
                    totalAmount = row[OrdersTable.totalAmount],
                    userName = row[UsersTable.name],
                )
            }
    }

// Aggregation
suspend fun countUsersByRole(): Map<Role, Long> =
    newSuspendedTransaction {
        UsersTable
            .select(UsersTable.role, UsersTable.id.count())
            .groupBy(UsersTable.role)
            .associate { row ->
                row[UsersTable.role] to row[UsersTable.id.count()]
            }
    }

// Subqueries
suspend fun findUsersWithOrders(): List<UserRow> =
    newSuspendedTransaction {
        UsersTable.selectAll()
            .where {
                UsersTable.id inSubQuery
                    OrdersTable.select(OrdersTable.userId).withDistinct()
            }
            .map { it.toUser() }
    }

// LIKE and pattern matching — always escape user input to prevent wildcard injection
private fun escapeLikePattern(input: String): String =
    input.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

suspend fun searchUsers(query: String): List<UserRow> =
    newSuspendedTransaction {
        val sanitized = escapeLikePattern(query.lowercase())
        UsersTable.selectAll()
            .where {
                (UsersTable.name.lowerCase() like "%${sanitized}%") or
                    (UsersTable.email.lowerCase() like "%${sanitized}%")
            }
            .map { it.toUser() }
    }
```

```
