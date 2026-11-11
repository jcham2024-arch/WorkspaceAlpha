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
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";

// Signer keys belong to the ORCHESTRATOR's env — never hardcoded, never agent-writable.
const evmKey = process.env.EVM_PRIVATE_KEY as `0x${string}`;
const svmKey = process.env.SVM_PRIVATE_KEY;
if (!evmKey || !svmKey) {
  throw new Error("Signer keys are not set — refusing to start payment client");
}

// One client, both network families: the buyer pays whichever chain the 402 offers.
const client = new x402Client();
client.register("eip155:*", new ExactEvmScheme(privateKeyToAccount(evmKey)));
client.register("solana:*", new ExactSvmScheme(await createKeyPairSignerFromBytes(base58.decode(svmKey))));

// A PaymentPolicy filters the SERVER's payment requirements before any
// signature is created. Returning an empty array means "nothing here is
// acceptable" and the client refuses to pay rather than falling back.
const ALLOWED_NETWORKS = new Set([
  "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",      // Solana mainnet
  "eip155:8453",                                   // Base
]);
const MAX_AMOUNT = 10_000n;      // atomic units, 6-decimal USDC: 0.01 USDC per call
const SESSION_CAP = 50_000n;     // 0.05 USDC across the whole session

// EVM addresses are case-insensitive, so compare them lowercased. Solana
// addresses are base58 and ARE case-sensitive — never lowercase those, or a
// different account could slip through.
const normalizeAddress = (a: string) => (a.startsWith("0x") ? a.toLowerCase() : a);
const ALLOWED_ASSETS = new Set(
  [
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  // USDC, Solana mainnet
    "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",    // USDC, Base
  ].map(normalizeAddress),
);
// Who you are willing to pay. Without this, any 402 an agent happens to hit
// can name its own recipient.
const ALLOWED_PAY_TO = new Set(
  ["7pr7NCaQRz5PEhPy7BAeB3Z72TVkiShhjRyVCN5DA6yC"].map(normalizeAddress),
);

client.registerPolicy((_x402Version, requirements) =>
  requirements.filter(r => {
    if (!ALLOWED_NETWORKS.has(r.network)) return false;                   // wrong chain
    if (!ALLOWED_ASSETS.has(normalizeAddress(r.asset))) return false;     // wrong token
    if (!ALLOWED_PAY_TO.has(normalizeAddress(r.payTo))) return false;     // wrong recipient
    try {
      const amount = BigInt(r.amount);
      return amount >= 0n && amount <= MAX_AMOUNT;                        // over budget / negative
    } catch {
      return false;                                                       // unparseable amount
    }
  }),
);

// The policy sees one challenge at a time, so it cannot enforce a session
// total or ask a human anything. Keep the payment-enabled client private and
// route every paid call through the payOnce boundary below.

// Supply this from your harness — a real prompt, never a stub that returns true.
declare function confirmWithUser(prompt: string): Promise<boolean>;

// Resource authorization is independent of recipient and budget policy.
// The ORCHESTRATOR supplies exact approved HTTPS origins before delegation;
// never populate this set from a server challenge or agent-controlled input.
const ALLOWED_ORIGINS = new Set(["https://api.example.com"]);
function requireAllowedOrigin(url: string): void {
  const parsed = new URL(url);
  if (!ALLOWED_ORIGINS.has(parsed.origin) || parsed.username || parsed.password) {
    throw new Error("Resource origin is not authorized");
  }
}

// Both approved assets above are 6-decimal USDC. Update this trusted formatting
// policy along with the asset allowlist if you support other assets/decimals.
const USDC_SCALE = 1_000_000n;
const humanUSDC = (amount: bigint) =>
  `${amount / USDC_SCALE}.${(amount % USDC_SCALE).toString().padStart(6, "0").replace(/0+$/, "") || "0"} USDC`;

let sessionSpent = 0n;
let sessionApproval: Promise<boolean> | undefined;

async function payOnce(url: string, init?: RequestInit): Promise<Response> {
  requireAllowedOrigin(url); // Before reservation, prompt, fetch, or signature.
  // Reserve the worst case the policy allows. Settlement responses do not
  // carry an amount, so counting MAX_AMOUNT per call is a deliberate
  // over-estimate — it can stop early, never late. Reserve before any await,
  // so concurrent calls cannot all pass the check.
  if (sessionSpent + MAX_AMOUNT > SESSION_CAP) {
    throw new Error("Session budget exhausted — blocked");
  }
  sessionSpent += MAX_AMOUNT;
  // Release the reservation only when no signed payment left this process:
  // a declined or failed prompt, a challenge the policy rejected, or a free
  // response. Once a signed request is sent it may settle, so keep it counted.
  let signedRequestSent = false;
  const trackingFetch: typeof fetch = async (input, reqInit) => {
    // Override caller options on BOTH the challenge and signed retry. Native
    // fetch refuses redirects, so an unauthorized host cannot return a 402
    // or receive a payment header via an automatic redirect.
    const req = new Request(input, { ...reqInit, redirect: "error" });
    requireAllowedOrigin(req.url);
    if (req.headers.has("PAYMENT-SIGNATURE") || req.headers.has("X-PAYMENT")) {
      signedRequestSent = true;
    }
    const response = await fetch(req);
    // Also fail closed for adapters that expose a redirect response instead.
    if (response.redirected || (response.status >= 300 && response.status < 400)) {
      throw new Error("Paid request redirects are blocked");
    }
    return response;
  };
  try {
    // Install one promise before awaiting the prompt. Concurrent calls share
    // the same decision, including a decline or failure; never auto-reprompt.
    sessionApproval ??= Promise.resolve().then(() => confirmWithUser(
      `Allow paid requests to origins: ${[...ALLOWED_ORIGINS].join(", ")}? ` +
      `Networks: ${[...ALLOWED_NETWORKS].join(", ")}. ` +
      `Assets: ${[...ALLOWED_ASSETS].join(", ")} (6-decimal USDC). ` +
      `Recipients (payTo): ${[...ALLOWED_PAY_TO].join(", ")}. ` +
      `Per-call cap: ${humanUSDC(MAX_AMOUNT)}; session cap: ${humanUSDC(SESSION_CAP)}.`,
    ));
    if (!await sessionApproval) {
      throw new Error("User declined: no payment attempted");
    }
    return await wrapFetchWithPayment(trackingFetch, client)(url, init);
  } finally {
    if (!signedRequestSent) sessionSpent -= MAX_AMOUNT;
  }
}

const res = await payOnce("https://api.example.com/data", { method: "GET" });
```

```
