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
class UserServiceTest : FunSpec({
    val repository = mockk<UserRepository>()
    val logger = mockk<Logger>(relaxed = true) // Relaxed: returns defaults
    val service = UserService(repository, logger)

    beforeTest {
        clearMocks(repository, logger)
    }

    test("findUser delegates to repository") {
        val expected = User(id = "1", name = "Alice")
        every { repository.findById("1") } returns expected

        val result = service.findUser("1")

        result shouldBe expected
        verify(exactly = 1) { repository.findById("1") }
    }

    test("findUser returns null for unknown id") {
        every { repository.findById(any()) } returns null

        val result = service.findUser("unknown")

        result.shouldBeNull()
    }
})
```

```
