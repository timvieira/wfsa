# Weighted Finite-State Automata

A Python library for weighted finite-state automata (WFSAs) over fields and semirings.

- **Field-weighted** (`wfsa.field_wfsa`): equivalence testing, minimization (forward/backward conjugates), and weight pushing for automata over fields (e.g., reals). Follows [Kiefer (2020)](https://arxiv.org/abs/2009.01217) closely.
- **Semiring-weighted** (`wfsa.semiring_wfsa`): determinization ([Mohri, 2009](https://link.springer.com/chapter/10.1007/978-3-642-01492-5_6)), Brzozowski minimization, and weight pushing for automata over arbitrary semirings.

## References

 - Stefan Kiefer (2020) [Notes on Equivalence and Minimization of Weighted Automata](https://arxiv.org/abs/2009.01217)
 - Mehryar Mohri (2009) [Weighted Automata Algorithms](https://link.springer.com/chapter/10.1007/978-3-642-01492-5_6)
