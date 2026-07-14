# Paper 1 Formal Specification

The shared working notation is defined in
[`../../shared/notation.md`](../../shared/notation.md). This file records the
Paper 1 decisions needed to turn that notation into a precise formalism.

## Definition checklist

- [ ] Supported base-graph types and attribute domains.
- [ ] Interpretation-graph node and edge semantics.
- [ ] Mapped-subgraph membership and overlap rules.
- [ ] Equality and isomorphism of Abstract Graph representations.
- [ ] Structural equivalence relation used by identities.
- [ ] Provenance representation and composition.
- [ ] Operator input, output, and failure contracts.
- [ ] Operator-program composition rules.
- [ ] Serialization semantics.

## Proof obligations or empirical substitutes

| Obligation | Method | Evidence artifact | Status |
| --- | --- | --- | --- |
| Mapping validity is preserved by every reference operator. | Proof plus property tests | Pending | Open |
| Provenance is complete after operator composition. | Induction over composition plus tests | Pending | Open |
| Identities are invariant under permitted relabelling. | Definition plus permutation tests | Pending | Open |
| Serialization preserves the representation. | Round-trip property tests | Pending | Open |
| Operator composition is closed for valid typed programs. | Type/contract argument plus tests | Pending | Open |
