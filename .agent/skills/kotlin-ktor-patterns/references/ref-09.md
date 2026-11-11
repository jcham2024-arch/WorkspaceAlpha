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
fun Route.authRoutes() {
    val authService by inject<AuthService>()

    route("/auth") {
        post("/login") {
            val request = call.receive<LoginRequest>()
            val token = authService.login(request.email, request.password)
                ?: return@post call.respond(
                    HttpStatusCode.Unauthorized,
                    ApiResponse.error<Unit>("Invalid credentials"),
                )
            call.respond(ApiResponse.ok(TokenResponse(token)))
        }

        post("/register") {
            val request = call.receive<RegisterRequest>()
            val user = authService.register(request)
            call.respond(HttpStatusCode.Created, ApiResponse.ok(user))
        }

        authenticate("jwt") {
            get("/me") {
                val userId = call.userId()
                val user = authService.getProfile(userId)
                call.respond(ApiResponse.ok(user))
            }
        }
    }
}
```

```
