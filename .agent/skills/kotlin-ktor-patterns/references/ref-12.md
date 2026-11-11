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
// di/AppModule.kt
val appModule = module {
    // Database
    single<Database> { DatabaseFactory.create(get()) }

    // Repositories
    single<UserRepository> { ExposedUserRepository(get()) }
    single<OrderRepository> { ExposedOrderRepository(get()) }

    // Services
    single { UserService(get()) }
    single { OrderService(get(), get()) }
    single { AuthService(get(), get()) }
}

// Application setup
fun Application.configureDI() {
    install(Koin) {
        modules(appModule)
    }
}
```

```
