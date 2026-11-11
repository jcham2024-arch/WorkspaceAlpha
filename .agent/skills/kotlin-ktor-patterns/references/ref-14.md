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
class UserServiceTest : FunSpec(), KoinTest {
    override fun extensions() = listOf(KoinExtension(testModule))

    private val testModule = module {
        single<UserRepository> { mockk() }
        single { UserService(get()) }
    }

    private val repository by inject<UserRepository>()
    private val service by inject<UserService>()

    init {
        test("getUser returns user") {
            coEvery { repository.findById("1") } returns testUser
            service.getById("1") shouldBe testUser
        }
    }
}
```

```
