---
name: agent-payment-x402
description: Add x402 payment execution to AI agents with per-task budgets, spending controls, and non-custodial wallets. Supports Base through agentwallet-sdk, X Layer through OKX Payments / OKX Agent Payments Protocol, and Solana plus multi-network EVM through the upstream x402 packages with facilitator-based settlement. Use when an agent must pay for something itself and needs per-task budgets, spending controls, and a non-custodial
metadata:
  origin: community
---

# Agent Payment Execution (x402)

Enable AI agents to make policy-gated payments with built-in spending controls. Uses the x402 HTTP payment protocol and MCP tools so agents can pay for external services, APIs, or other agents without custodial risk.

## When to Use

Use when: your agent needs to pay for an API call, purchase a service, settle with another agent, enforce per-task spending limits, or manage a non-custodial wallet. Pairs naturally with cost-aware-llm-pipeline and security-review skills.

## Decision Tree

Choose the integration path based on whether your agent is buying access to a paid API or charging others for one:

| Need | Recommended path |
|------|------------------|
| Agent pays a 402-gated API on Base or another agentwallet-supported chain | Use `agentwallet-sdk` as an MCP payment server with strict spending policy |
| Agent pays a 402-gated API on X Layer | Use OKX Agent Payments Protocol from `okx/onchainos-skills`; `okx-x402-payment` is a deprecated legacy alias |
| Agent pays a 402-gated API on Solana or another x402 v2 network | Wrap the agent's HTTP client with the upstream `@x402/fetch` or `@x402/axios` package and register the EVM/SVM schemes; the resource server's facilitator verifies and settles |
| API charges agents on Solana or multiple networks (TypeScript, Python, or Go) | Use the upstream x402 middleware from `x402-foundation/x402` — `@x402/express`, `@x402/hono`, `@x402/next`, or `@x402/fastify` for TypeScript, `x402` for Python, `github.com/x402-foundation/x402/go/v2` for Go |
| TypeScript API charges agents | Use OKX Payments TypeScript seller SDK docs for Express, Hono, Fastify, or Next.js |
| Go API charges agents | Use OKX Payments Go seller SDK docs for Gin, Echo, or `net/http` |
| Rust API charges agents | Use OKX Payments Rust seller SDK docs for Axum |
| Java API charges agents | Use OKX Payments Java seller SDK docs for Spring Boot 2/3, Java EE, or Jakarta |
| Python API charges agents | Check the current OKX Payments repository before implementation; a Python seller guide may not be available |

## Supported Networks

- `agentwallet-sdk`: use the package docs to confirm current network coverage before production. Base Sepolia is the safest development default; Base mainnet is the production path called out by the original skill.
- OKX Payments / X Layer: current seller docs target X Layer (`eip155:196`) and USDT0 settlement. Fetch current SDK docs before generating production code because payment packages and facilitator behavior can change quickly.
- Upstream x402 packages: multi-network by design — one route can advertise Base and Solana simultaneously and let the buyer pick. The packages default to the `x402.org` facilitator, which is testnet-only (Base Sepolia `eip155:84532`, Solana devnet `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1`, plus Stellar, Aptos, Hedera, and XRPL testnets) and is not intended for mainnet routes. For mainnet (`solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` for Solana), either self-facilitate, run your own facilitator, or pick a hosted one from the upstream facilitator list — see the facilitator comparison under Option C. Confirm live coverage at the facilitator's `/supported` endpoint before production rather than hardcoding it here.

## How It Works

### x402 Protocol
x402 extends HTTP 402 (Payment Required) into a machine-negotiable flow. When a server returns `402`, the agent's payment tool negotiates price, checks budget, signs a transaction, and retries only inside the policy and confirmation boundary set by the orchestrator.

### Spending Controls
Every payment tool call enforces a `SpendingPolicy`:
- **Per-task budget** — max spend for a single agent action
- **Per-session budget** — cumulative limit across an entire session
- **Allowlisted recipients** — restrict which addresses/services the agent can pay
- **Rate limits** — max transactions per minute/hour

### Non-Custodial Wallets
Agents hold their own keys via ERC-4337 smart accounts. The orchestrator sets policy before delegation; the agent can only spend within bounds. No pooled funds, no custodial risk.

## MCP Integration

The payment layer exposes standard MCP tools that slot into any Claude Code or agent harness setup.

> **Security note**: Always pin the package version. This tool manages private keys — unpinned `npx` installs introduce supply-chain risk.

### Option A: agentwallet-sdk (Base / multi-chain)


### Available Tools (agent-callable)

| Tool | Purpose |
|------|---------|
| `get_balance` | Check agent wallet balance |
| `send_payment` | Send payment to address or ENS |
| `check_spending` | Query remaining budget |
| `list_transactions` | Audit trail of all payments |

> **Note**: Spending policy is set by the **orchestrator** before delegating to the agent — not by the agent itself. This prevents agents from escalating their own spending limits. Configure policy via `set_policy` in your orchestration layer or pre-task hook, never as an agent-callable tool.

### Option B: OKX Agent Payments Protocol (X Layer)

Use this path for X Layer x402, Multi-Party Payment (MPP), session payment, charge, and A2A charge flows.

For buyer-side agent flows:

1. Install or reference the current `okx/onchainos-skills` repository.
2. Use `skills/okx-agent-payments-protocol/SKILL.md` as the dispatcher.
3. Treat `skills/okx-x402-payment/SKILL.md` as a deprecated compatibility alias, not as the canonical skill.
4. Require explicit user confirmation before wallet status checks or payment actions. Do not hide payment execution behind a generic tool call.

For seller-side API flows, fetch the latest language-specific guide before generating code:

| Runtime | Current guide |
|---------|---------------|
| TypeScript | `https://raw.githubusercontent.com/okx/payments/main/typescript/SELLER.md` |
| Go | `https://raw.githubusercontent.com/okx/payments/main/go/x402/SELLER.md` |
| Rust | `https://raw.githubusercontent.com/okx/payments/main/rust/x402/SELLER.md` |
| Java | `https://raw.githubusercontent.com/okx/payments/main/java/SELLER.md` |

Do not copy examples from older docs without checking the current OKX repository. Current OKX guidance uses `okx-agent-payments-protocol` as the dispatcher, and Java seller docs are now available.

### Option C: Upstream x402 packages (Solana + Base/EVM)

Use this path when the agent pays — or your API charges — on Solana, Base, or another network the upstream protocol implementation supports. The canonical x402 monorepo at [`x402-foundation/x402`](https://github.com/x402-foundation/x402) is actively maintained and publishes the client and middleware packages directly. Unlike Options A and B this is not a separate MCP server — you wrap the agent's own HTTP client, and a facilitator chosen by the resource server verifies and settles.

For buyer-side agent flows:

1. Start from the maintained examples in [`examples/typescript/clients`](https://github.com/x402-foundation/x402/tree/main/examples/typescript/clients) (fetch, axios, MCP) rather than copying snippets from older docs.
2. Require explicit user confirmation before signing or submitting the first paid request, exactly as Option B requires for OKX flows. Do not hide payment execution behind a generic tool call.
3. Pin package versions (for example `@x402/fetch@2.22.0`); all upstream packages version in lockstep.
4. Enforce your budget with a `PaymentPolicy` registered on the client, so the check runs against the server's actual challenge on every call. A budget compared against a number you passed in yourself proves nothing — the amount, asset, and network all come from the server, so all three must be validated before a signature exists.

5. Configure an exact resource-origin allowlist separately from recipient and budget policy. All payment-enabled fetches below refuse redirects. Session approval names the approved origins, networks, assets, recipients, and human-unit spending caps; concurrent calls share one decision. Keep this client and its policy private to the orchestrator.


With the policy registered, an over-budget amount, an unexpected token, or an unregistered chain all fail closed — `createPaymentPayload` throws instead of signing, because every candidate was filtered out. Devnet USDC is `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`; add it to `ALLOWED_ASSETS` only for development. Test the policy adversarially — feed it a challenge demanding `5000000` atomic units, one quoting a different mint, and one on a chain you never registered, and assert that none of them produce a signature. In the exact-SVM scheme the facilitator is the transaction fee payer, so the buyer wallet holds USDC only — no SOL for gas.

**Facilitator choice.** A facilitator verifies and settles on the resource server's behalf, so this is the resource server's decision, not the buyer's. In rough order of least to most trust delegated:

| Option | When it fits |
|--------|--------------|
| [Self-facilitate in-process](https://github.com/x402-foundation/x402/tree/main/examples/typescript/servers/self-facilitation) | You want no third party in the settlement path and can hold keys and RPC access yourself |
| Run your own facilitator | You want that same control but shared across several services |
| [`x402.org` facilitator](https://x402.org/facilitator) | Development and testnets — it is the package default, requires no setup, and upstream documents it as not intended for mainnet routes |
| A hosted production facilitator | You want mainnet coverage without operating infrastructure |

For the hosted option, choose from the [facilitator list](https://docs.x402.org/dev-tools/facilitators) in the upstream docs rather than a name copied from here — it is maintained, it is not exhaustive, and coverage changes. As of writing it includes Coinbase's CDP (KYT/OFAC screening on every transaction), PayAI, Corbits, Dexter, Solvador, and others; several cover Solana mainnet alongside EVM. Whichever you pick, confirm live coverage at its `/supported` endpoint before production and re-check when you add a network.

> **Disclosure**: this section was contributed by someone who works on PayAI, one of the listed facilitators. It is included as one option among several, and the self-hosted and upstream-default paths above are deliberately listed first.

**Seller side (API charges agents).** Use the upstream middleware; one route can advertise Base and Solana simultaneously (see [`examples/typescript/servers`](https://github.com/x402-foundation/x402/tree/main/examples/typescript/servers) for runnable versions):

| Runtime | Package |
|---------|---------|
| Express / Hono / Next.js / Fastify | `@x402/express@2.22.0`, `@x402/hono@2.22.0`, `@x402/next@2.22.0`, `@x402/fastify@2.22.0` |
| Python (FastAPI, Flask) | `x402` on PyPI |
| Go (Gin, Echo, `net/http`) | `github.com/x402-foundation/x402/go/v2` |

**Solana sellers: the `payTo` address needs its canonical token account first.** The exact-SVM client derives the *associated token account* (ATA) for `payTo` with `findAssociatedTokenPda` and transfers there; it never creates it. If that exact account is missing, settlement fails at simulation and the 402 comes back with `transaction_simulation_failed`, which reads like a client bug rather than a missing recipient account. Check the derived address itself — scanning the owner's token accounts is not equivalent, because a non-canonical auxiliary account for the same mint would pass while the ATA the client targets is still absent:


Then confirm that exact address exists — `value: null` means it does not, and settlement to it will fail:


To provision it (whoever creates it pays the small rent, not the payer):

- In code, add `getCreateAssociatedTokenIdempotentInstruction` from `@solana-program/token` to your onboarding flow — the idempotent variant is safe to re-run and is the only option that is deterministic.
- `spl-token create-account <MINT> --owner <PAYTO_ADDRESS>` with the spl-token CLI.
- A transfer of that token to `payTo` also works, but only when the sender includes the create instruction — wallets and `spl-token transfer --fund-recipient` do; a bare `transferChecked` to a missing ATA fails the same way settlement does.

This bites hardest when payouts go to freshly provisioned or custodial wallets, which often have no ATA for the asset yet.

**Sellers: run the route once per payment authorization.** The middleware verifies the payment, runs your handler, then settles. Verification does not consume the authorization (settlement does), so one signed payment sent several times at once passes verify every time and runs your handler every time. The facilitator settles only one copy, and the others get a 402 without the response, so nobody receives free output. But every side effect in the handler (an LLM call, a queued job, an on-chain transaction) happens once per copy. On a production seller (Python `x402` 2.9.0, FastAPI), one authorization sent three times concurrently produced three handler runs and one settlement. A paid-call counter inside the handler overstates revenue the same way; count after settlement instead. The wider verify-to-settle race is discussed in [x402#1169](https://github.com/x402-foundation/x402/issues/1169).

Claim each authorization once, after the facilitator has verified it and before the handler runs. The resource server's `onAfterVerify` hook runs at exactly that point, and an `abort` from it becomes a 402 without running the handler:


Any store with an atomic conditional insert works: DynamoDB `PutItem` with `attribute_not_exists`, or a unique index in Postgres. Two things the guard does not decide for you. If the store is down, `FAIL_CLOSED` keeps the once-per-authorization guarantee at the cost of availability; failing open keeps the route up but lets every copy run the handler until the store recovers, so use it only for idempotent handlers. And `payment_replayed` means the authorization was presented before, not that the first attempt failed: if the client lost the first response, the work may have run and the payment may have settled, so it should reconcile the original request before signing a new authorization. This closes duplicate copies of one authorization only. A payer who invalidates the payment between verify and settle (for example by moving the funds) still gets one handler run; for expensive routes, hold funds before doing the work.

**Discovery.** Facilitators that implement the x402 bazaar extension expose a `/discovery/resources` endpoint — query the CDP catalog at `https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources` and the PayAI catalog at `https://facilitator.payai.network/discovery/resources`. For Solana-payable services there is also [pay.sh](https://pay.sh), the Solana Foundation's curated catalog.

## Examples

### Budget enforcement in an MCP client

When building an orchestrator that calls the agentpay MCP server, enforce budgets before dispatching paid tool calls.

> **Prerequisites**: Install the package before adding the MCP config — `npx` without `-y` will prompt for confirmation in non-interactive environments, causing the server to hang: `npm install -g agentwallet-sdk@6.0.0`


## Best Practices

- **Set budgets before delegation**: When spawning sub-agents, attach a SpendingPolicy via your orchestration layer. Never give an agent unlimited spend.
- **Pin your dependencies**: Always specify an exact version in your MCP config (e.g., `agentwallet-sdk@6.0.0`). Verify package integrity before deploying to production.
- **Audit trails**: Use `list_transactions` in post-task hooks to log what was spent and why.
- **Fail closed**: If the payment tool is unreachable, block the paid action — don't fall back to unmetered access.
- **Pair with security-review**: Payment tools are high-privilege. Apply the same scrutiny as shell access.
- **Test with testnets first**: Use Base Sepolia for development; switch to Base mainnet for production. On Solana, develop against Solana devnet (`solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1`) and the free x402.org facilitator before moving to a production facilitator on mainnet.
- **On Solana, fund USDC not SOL**: The exact-SVM scheme makes the facilitator the transaction fee payer, so a SOL-less wallet still pays. Verify each challenge's `asset` against the expected USDC mint (mainnet `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`, devnet `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`) before signing — a wrapped client that pays any asset is a hole in your budget.

## Production Reference

- **npm**: [`agentwallet-sdk`](https://www.npmjs.com/package/agentwallet-sdk)
- **Merged into NVIDIA NeMo Agent Toolkit**: [PR #17](https://github.com/NVIDIA/NeMo-Agent-Toolkit-Examples/pull/17) — x402 payment tool for NVIDIA's agent examples
- **Protocol spec**: [x402.org](https://x402.org)
- **OKX Payments SDKs**: [`okx/payments`](https://github.com/okx/payments) — TypeScript, Go, Rust, and Java seller integrations for X Layer x402
- **OKX Agent Payments Protocol skill**: [`okx/onchainos-skills`](https://github.com/okx/onchainos-skills/tree/main/skills/okx-agent-payments-protocol)
- **OKX Payments overview**: [web3.okx.com/onchainos/dev-docs/payments/overview](https://web3.okx.com/onchainos/dev-docs/payments/overview)
- **Upstream x402 monorepo**: [`x402-foundation/x402`](https://github.com/x402-foundation/x402) — TypeScript, Python, and Go implementations plus maintained client and server examples
- **x402 docs**: [docs.x402.org](https://docs.x402.org); production facilitator list at [docs.x402.org/dev-tools/facilitators](https://docs.x402.org/dev-tools/facilitators)
- **`@x402` packages**: [npmjs.com/org/x402](https://www.npmjs.com/org/x402) — `@x402/fetch`, `@x402/axios`, `@x402/express`, `@x402/hono`, `@x402/next`, `@x402/fastify`, `@x402/evm`, `@x402/svm`
- **Facilitators**: [self-facilitation example](https://github.com/x402-foundation/x402/tree/main/examples/typescript/servers/self-facilitation) (no third party), [x402.org facilitator](https://x402.org/facilitator) (testnet default), and the maintained [production list](https://docs.x402.org/dev-tools/facilitators)
- **Discovery**: CDP and PayAI bazaars at `/discovery/resources`; [pay.sh](https://pay.sh) for Solana-payable services
