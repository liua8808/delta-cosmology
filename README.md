# Delta Cosmology (Δ-Cosmology)
### A Pre-Theoretical Framework for Difference-Grounded Physics

**Working Paper v0.3** · 2026

---

## One-Line Summary

The complex Hilbert space of quantum mechanics is not a postulate —
it is the unique stable geometry forced upon any physical theory satisfying five structural requirements about how differences compose, transform, and interfere.

---

## What This Is

This repository contains a working paper and supporting code for **Delta Cosmology**,
a pre-theoretical framework in which *difference* — the bare capacity for two states to be distinguished — is taken as the ontological primitive, prior to information, probability, or Hilbert space.

**This is not a finished theory.** It is a framework with a clear conjecture, a known argument structure, identified gaps, and the first numerical evidence. It is positioned at the boundary between philosophy of physics and quantum foundations.

---

## The Central Conjecture

> **Conjecture Δ-C:**
> If a physical theory satisfies conditions T, C, E, R, and I,
> then its minimal stable state space representation necessarily carries a complex Hilbert structure.

Where:

| Condition | Meaning |
|-----------|---------|
| **T** | Continuous isometric transitivity — states are related by a continuous symmetry group |
| **C** | Compositional closure — composite systems are still physical systems |
| **E** | Non-locally decomposable difference patterns exist (pre-linear generalization of entanglement) |
| **R** | Continuous reversible dynamics |
| **I** | Interference-consistent probability — different paths can cancel, yielding consistent probabilities |

The constraint chain:

```
Raw difference structure
  ↓ T
Symmetric manifold
  ↓ C
Projective-type state space
  ↓ E
Classical separable structures excluded
  ↓ R
Real structures develop topological obstructions
  ↓ I
Quaternionic structures excluded
  ↓
Complex Hilbert space
```

**Current status of the conjecture:** The argument structure is complete. Two steps require further mathematical rigorization: the precise exclusion of real structures by R (Lie group orbit analysis), and the precise exclusion of quaternionic structures by I (probability consistency under non-commutative composition).

---

## Key Definitions

**Difference structure:** A function Δ: Ω × Ω → ℝ⁺ satisfying Δ(A,A) = 0 and Δ(A,B) = Δ(B,A). *No triangle inequality is assumed.* This is weaker than a metric.

**Condition E (precise):** A composite difference structure (Ω₁₂, Δ₁₂) is non-locally indecomposable if there do not exist projection maps π₁, π₂ and a function f such that:
```
Δ₁₂(A,B) = f(Δ₁(π₁A, π₁B), Δ₂(π₂A, π₂B))
```
This is defined *without* presupposing linear structure. Quantum entanglement is a special case of E, but E is strictly broader.

**The divergence point:** The triangle inequality is the boundary between Hilbert-embeddable and non-Hilbert-embeddable difference structures (Schoenberg's theorem). If physical systems exist whose distinguishability violates the triangle inequality, they lie outside standard quantum mechanics but inside the Δ framework.

---

## Numerical Toy Model

The file `delta_toy.py` constructs a minimal model on S¹ demonstrating that T and E can be satisfied while Hilbert embeddability fails.

| Structure | T | E | Triangle ineq. | Hilbert-embeddable |
|-----------|---|---|---------------|-------------------|
| Chord distance | ✓ | ✓ | ✓ | ✓ (baseline) |
| Angular distance | ✓ | ✓ | ✓ | ✗ (known geometry) |
| Superlinear Δ, α=1.8 | ✓ | ✓ | ✗ (29% violated) | ✗ (confirmed) |

Run the model:
```bash
python delta_toy.py
```

---

## Repository Contents

| File | Description |
|------|-------------|
| `delta_cosmology_paper_en.docx` | Full English working paper (10 sections) |
| `delta_cosmology_v0.3.docx` | Full Chinese working record with all derivations |
| `delta_cosmology_abstract_v0.2.pdf` | One-page formal abstract (suitable for sharing) |
| `delta_toy.py` | Numerical toy model — runs immediately |
| `delta_toy_v2.png` | Numerical results figure |

---

## Relation to Existing Work

This framework is closest to Hardy's quantum reconstruction (2001), but starts from a weaker primitive: difference rather than information capacity. The complex number field is forced out by the same mechanism (continuous reversible transformations), but the starting point defers the probabilistic structure further.

Other related frameworks: Stueckelberg (1960), Rovelli's relational QM (1996), Chiribella-D'Ariano-Perinotti (2011), General Probabilistic Theories, Zurek's algorithmic thermodynamics (1989).

The distinctive feature of Δ-Cosmology: condition E is defined without presupposing linear structure, making it potentially broader than standard entanglement. Whether this breadth is physically realized is the key open question.

---

## Open Problems

1. **Complete Conjecture Δ-C** — rigorize the exclusion of real structures (R) and quaternionic structures (I)
2. **Physical test of the divergence point** — find experimental systems where distinguishability violates the triangle inequality (context-dependent measurement in quantum optics is a candidate)
3. **Low-entropy initial conditions** — does the Δ framework constrain cosmological initial conditions?

---

## About

This framework was developed in a series of conversations exploring whether the mathematical structure of quantum mechanics could be derived from something more primitive than Hilbert space.

The author is a pediatric physician, not a professional physicist. This paper is offered in the spirit of open inquiry. Criticism, engagement, and collaboration are welcome.

> *If this framework has value, its value is not in providing final answers,*
> *but in providing a new way of asking questions.*

---

## License

This work is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
You are free to share and adapt with attribution.
