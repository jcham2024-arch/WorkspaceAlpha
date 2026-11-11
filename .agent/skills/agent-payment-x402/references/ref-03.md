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
import { findAssociatedTokenPda, TOKEN_PROGRAM_ADDRESS } from "@solana-program/token";

const [ata] = await findAssociatedTokenPda({
  mint: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",   // USDC mainnet
  owner: payToAddress,
  tokenProgram: TOKEN_PROGRAM_ADDRESS,                     // TOKEN_2022_PROGRAM_ADDRESS for Token-2022 mints
});
```

```
