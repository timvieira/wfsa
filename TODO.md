# TODO

## Mathematical Correctness & Robustness

- [ ] **Gram-Schmidt numerical stability**: `proj()` uses classical Gram-Schmidt, which is numerically unstable. Switch to modified Gram-Schmidt (orthogonalize against updated vectors, not originals).
- [ ] **Division by zero in `proj()`**: `(q @ q)` can be near-zero for near-dependent vectors, producing `inf`/`nan`. Add a tolerance check and skip near-zero projections.
- [ ] **`approx_equal` tolerance**: Hardcoded via `np.allclose` defaults (`atol=1e-8`). Consider making tolerance configurable, especially for ill-conditioned automata or long strings where error accumulates.
- [ ] **`Simple.__hash__` returns constant 0**: Every `Simple` instance hashes identically, making any dict/set of them O(n). The commented-out randomized hash (based on [arXiv:1302.2818](https://arxiv.org/abs/1302.2818)) is a good direction — worth finishing.
- [ ] **`counterexample()` basis test is inverted**: The check should arguably be on the residual norm, not on whether `u` changed (a vector can change but still be nearly dependent). Consider `np.linalg.norm(u - q) > tol` instead.
- [ ] **`star()` convergence for semirings**: `_lehmann` calls `R.star()` which computes `(1-x)^{-1}` — valid for reals with `|x|<1`, but no convergence check. Document the precondition or add a guard.
- [ ] **Weight pushing assumes invertibility**: `push` inverts backward weights with `V[i]**(-1)`. The zero check guards the outer loop but not individual arc weights mixing zero/nonzero. Document that pushing requires the weight semiring to be a group (or at minimum a division ring).

## Algorithmic Efficiency

- [ ] **Lehmann's algorithm is O(n^3) per symbol**: `_lehmann` iterates all (i,k) pairs for each pivot j. For sparse automata, use sparse representations or adjacency-list iteration instead of dense N x N.
- [ ] **`Simple` always builds dense matrices**: Creates `np.full((S,S), ...)` for every symbol. For automata with large state spaces but sparse transitions, use `scipy.sparse`.
- [ ] **`to_wfsa` iterates all (i,j) pairs**: Triple nested loop including zero entries. Skip entries where `arcs[a][i,j]` is zero.
- [ ] **`epsremove` is O(|Q|^2) in new arcs**: Iterates all states `k` for every arc, even when `S[j,k]` is zero. Filter on nonzero entries of the closure.
- [ ] **`trim` computes both `forward()` and `backward()`, each invoking `_lehmann`**: These share the same transitive closure `K`. Factor out `K` computation to avoid recomputing it.
- [ ] **Determinization creates `frozendict` states**: Builds `frozendict` for each power-set state. For large nondeterministic automata this can blow up exponentially (inherent to subset construction, but consider adding a state-count limit with a clear error).

## Test Coverage

- [ ] **Edge cases**: empty automaton, single-state automaton, epsilon-only automaton
- [ ] **Numerical stress tests**: near-zero weights, very large/small weight ratios, long strings (error accumulation)
- [ ] **Round-trip tests**: `to_wfsa` ∘ `simple` should preserve the language (modulo epsilon); test this systematically
- [ ] **`push` correctness**: verify pushed automaton computes the same language as the original
- [ ] **`threshold` tests**: verify pruning preserves the language for weights above threshold
- [ ] **`reverse` ∘ `reverse` = identity** (up to renaming)
- [ ] **`star`, `kleene_plus` correctness**: test against brute-force enumeration for small alphabets
- [ ] **Semiring determinization non-termination**: add a timeout or max-states guard in tests so a broken `determinize` doesn't hang CI
- [ ] **`from_strings` test**: add a test for `from_strings` (was broken, now fixed)

## Code Quality

- [x] `base.py` raises `NotImplementedError` for `arcs(a=..., i=None)` — implemented
- [x] Duplicated `push` implementation in `field_wfsa.py` and `semiring_wfsa.py` — factored into `base.py`
- [ ] `WFSA.zero` and `WFSA.one` are set as class attributes by assignment after class definition (`field_wfsa.py:143-144`), overriding the `@property` in `base.py`. This means `instance.zero` returns the Float-valued class constant instead of respecting `instance.R`. Options:

  1. **Module-level constants**: Remove class assignment, export `zero`/`one` from `wfsa/__init__.py` directly. Base `@property` handles instance access.
     - Pro: Simple, no new abstractions.
     - Con: Changes public API (`WFSA.zero` → `wfsa.zero`). Tests and `__init__.py` need updating.

  2. **Custom descriptor**: A `__get__` that returns a default for class access (`WFSA.zero`) and delegates to `self.R` for instance access (`instance.zero`).
     - Pro: Both `WFSA.zero` and `instance.zero` work correctly.
     - Con: Adds a new descriptor class for two attributes.

  3. **`__init_subclass__` hook**: Base class sets `cls.zero = cls(R=...)` on each subclass.
     - Pro: Automatic for new subclasses.
     - Con: Requires each subclass to declare a default semiring. Still overrides the property (same bug for non-default R instances).

  4. **Leave as-is, document the limitation**: `WFSA.zero`/`WFSA.one` are Float-specific conveniences; `self.zero`/`self.one` from `base.py` only work if no subclass overrides them.
     - Pro: No code change.
     - Con: `self.one` in `base.py:star()` silently returns the wrong semiring if `self.R != Float`.
