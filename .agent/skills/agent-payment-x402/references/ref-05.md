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
```typescript
import { createHash } from "node:crypto";
import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { HTTPFacilitatorClient } from "@x402/core/server";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { getBase64Encoder, getTransactionDecoder } from "@solana/kit";
import { createClient } from "redis";

// Use a shared, durable, non-evicting claim store. Atomic insertion alone
// does not preserve claims after a store reset or eviction; test that operational
// contract separately before claiming durable replay protection.
// The claim store must never be what takes the seller down. With the offline
// queue disabled, a command sent while disconnected fails at once; the queue
// cap does the same when the store is connected but not replying; the error
// listener stops a client error from crashing the process; and the connection
// is made in the background, so startup never waits on it.
const redis = createClient({
  url: process.env.REDIS_URL,
  disableOfflineQueue: true,
  commandsQueueMaxLength: 1_000,
  socket: { connectTimeout: 2_000 },
});
redis.on("error", (err) => console.warn(`replay store: ${err.message}`));
redis.connect().catch(() => {});

const CLAIM_MIN_S = 900;          // longer than maxTimeoutSeconds plus your slowest handler run
const CLAIM_MAX_S = 366 * 86_400; // ceiling for a signer-chosen expiry
const CLAIM_TIMEOUT_MS = 250;     // a slow store must not stall paid requests
// When the store is unavailable: refuse before the handler runs (true), or run
// it without duplicate protection (false). Fail open only if the handler is
// idempotent or has its own side-effect boundary.
const FAIL_CLOSED = true;

// Identifies a verified authorization, however its JSON is encoded, and keeps
// the claim until the authorization can no longer settle: the signer picks
// that expiry, and verification does not cap it at maxTimeoutSeconds.
function claimOf(
  paymentPayload: { payload: Record<string, any> },
  requirements: { network: string; asset: string },
): { key: string; until: number } | undefined {
  const now = Math.floor(Date.now() / 1000);
  const keep = (expiry: unknown) => {
    // Reject authorizations beyond our retention contract; never shorten a
    // live authorization's claim lifetime and silently reopen its replay window.
    const validUntil = BigInt(String(expiry));
    if (validUntil < 0n || validUntil + 60n > BigInt(now + CLAIM_MAX_S)) {
      throw new Error("Authorization expiry exceeds the replay retention horizon");
    }
    return Math.max(now + CLAIM_MIN_S, Number(validUntil + 60n));
  };
  const p = paymentPayload.payload;
  if (p.authorization?.nonce) {
    // EVM exact, EIP-3009: each token contract accepts a (from, nonce) once.
    const { from, nonce, validBefore } = p.authorization;
    const asset = requirements.asset.toLowerCase();
    return {
      key: `x402:${requirements.network}:${asset}:${from.toLowerCase()}:${nonce.toLowerCase()}`,
      until: keep(validBefore),
    };
  }
  if (p.permit2Authorization?.nonce !== undefined) {
    // EVM exact, Permit2: uint256 nonces per owner, across tokens. The signed
    // value is BigInt(nonce), so "1", "01" and "0x1" are one authorization.
    const { from, nonce, deadline } = p.permit2Authorization;
    return {
      key: `x402:${requirements.network}:permit2:${from.toLowerCase()}:${BigInt(nonce)}`,
      until: keep(deadline),
    };
  }
  if (typeof p.transaction === "string") {
    // SVM exact: hash the message the payer signed, not the whole transaction.
    // The fee payer's signature slot is outside the payer's signature.
    const tx = getTransactionDecoder().decode(getBase64Encoder().encode(p.transaction));
    const digest = createHash("sha256").update(new Uint8Array(tx.messageBytes)).digest("hex");
    return { key: `x402:${requirements.network}:${digest}`, until: now + CLAIM_MIN_S };
  }
  return undefined;
}

function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  return Promise.race([
    promise,
    new Promise<T>((_, reject) => setTimeout(reject, ms, new Error("timeout")).unref()),
  ]);
}

const resourceServer = new x402ResourceServer(
  new HTTPFacilitatorClient({ url: process.env.FACILITATOR_URL }),
)
  .register("eip155:8453", new ExactEvmScheme())
  .onAfterVerify(async ({ paymentPayload, requirements, result }) => {
    if (!result.isValid) return; // an invalid payment never takes a claim
    let claim: ReturnType<typeof claimOf>;
    let set: Promise<string | null> | undefined;
    try {
      claim = claimOf(paymentPayload, requirements);
      if (!claim) {
        return { abort: true, reason: "claim_unsupported", message: "Authorization cannot be guarded." };
      }
      // NX is atomic: of two simultaneous copies exactly one wins.
      set = redis.set(claim.key, "1", {
        condition: "NX",
        expiration: { type: "EXAT", value: claim.until },
      });
      if ((await withTimeout(set, CLAIM_TIMEOUT_MS)) === "OK") return;
      return {
        abort: true,
        reason: "payment_replayed",
        message: "This payment authorization was already presented.",
      };
    } catch {
      // Return, don't throw: the resource server logs and skips a hook that
      // throws, which would run the handler unguarded.
      if (FAIL_CLOSED) {
        // A write that timed out can still land. This request is refused and
        // the handler never runs, so release a late claim, or the retry
        // would be refused as a replay of work that never happened.
        set?.then((reply) => (reply === "OK" && claim ? redis.del(claim.key) : 0)).catch(() => {});
        return { abort: true, reason: "claim_unavailable", message: "Retry shortly." };
      }
    }
  });

const app = express();
app.use(express.json());
app.use(
  paymentMiddleware(
    {
      "POST /report": {
        accepts: [{ scheme: "exact", price: "$0.01", network: "eip155:8453", payTo: process.env.PAY_TO! }],
      },
    },
    resourceServer,
  ),
);
app.post("/report", async (req, res, next) => {
  try {
    res.json(await buildReport(req.body));
  } catch (error) {
    // Keep the claim: a failed handler may already have performed side effects.
    next(error);
  }
});
```

```
