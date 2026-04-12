# TODO

## Packaging & Project Setup

- [x] Migrate `setup.py` to `pyproject.toml` (PEP 621)
- [x] Fix `project_url` (should be `project_urls` dict) and add `author_email`
- [x] Add missing dependencies: `semirings`, `frozendict`, `leftcorner` (needed by semiring module and tests)
- [x] Don't list `pytest` in `install_requires` — move to `[project.optional-dependencies]` or `[tool.pytest]`
- [x] Add a `LICENSE` file
- [x] Clean up stale `wfsa.egg-info/` and `__pycache__` (add to `.gitignore`)

## CI

- [x] Add GitHub Actions workflow: run tests on push (`pytest test/`)
- [x] Add a linting step (ruff)
- [x] Add a matrix for Python 3.10+ versions

## Mathematical Correctness & Robustness

- [ ] **Gram-Schmidt numerical stability**: `proj()` (`field_wfsa.py:319-324`) uses classical Gram-Schmidt, which is numerically unstable. Switch to modified Gram-Schmidt (orthogonalize against updated vectors, not originals).
- [ ] **Division by zero in `proj()`**: `(q @ q)` can be near-zero for near-dependent vectors, producing `inf`/`nan`. Add a tolerance check and skip near-zero projections.
- [ ] **`approx_equal` tolerance**: Hardcoded via `np.allclose` defaults (`atol=1e-8`). Consider making tolerance configurable, especially for ill-conditioned automata or long strings where error accumulates.
- [ ] **`Simple.__hash__` returns constant 0**: Every `Simple` instance hashes identically, making any dict/set of them O(n). The commented-out randomized hash (based on [arXiv:1302.2818](https://arxiv.org/abs/1302.2818)) is a good direction — worth finishing.
- [ ] **`counterexample()` basis test is inverted**: Line 231 checks `not approx_equal(u - q, u)` — this adds to the basis when the projection *changed* `u`, but the variable name `q` shadows the loop variable in `proj()`. More importantly, the check should arguably be on the residual norm, not on whether `u` changed (a vector can change but still be nearly dependent). Consider `np.linalg.norm(u - q) > tol` instead.
- [x] **`from_strings` missing initial/final weights**: `base.py:302-305` calls `m.add_I(xs[:0])` and `m.add_F(xs)` with no weight argument — these calls are missing the weight `w` (compare with `from_string` which passes `R.one`).
- [ ] **`star()` convergence for semirings**: `_lehmann` calls `R.star()` which computes `(1-x)^{-1}` — valid for reals with `|x|<1`, but no convergence check. Document the precondition or add a guard.
- [ ] **Weight pushing assumes invertibility**: `push` (`field_wfsa.py:130-132`, `semiring_wfsa.py:86-88`) inverts backward weights with `V[i]**(-1)`. The zero check guards the outer loop but not individual arc weights mixing zero/nonzero. Document that pushing requires the weight semiring to be a group (or at minimum a division ring).

## Algorithmic Efficiency

- [ ] **Lehmann's algorithm is O(n^3) per symbol**: `_lehmann` (`base.py:10-29`) iterates all (i,k) pairs for each pivot j. For sparse automata, use sparse representations or adjacency-list iteration instead of dense N x N.
- [ ] **`Simple` always builds dense matrices**: `field_wfsa.py:75-76` creates `np.full((S,S), ...)` for every symbol. For automata with large state spaces but sparse transitions, use `scipy.sparse`.
- [ ] **`to_wfsa` iterates all (i,j) pairs**: `field_wfsa.py:307-309` has a triple nested loop including zero entries. Skip entries where `arcs[a][i,j]` is zero.
- [ ] **`epsremove` is O(|Q|^2) in new arcs**: `base.py:169-172` iterates all states `k` for every arc, even when `S[j,k]` is zero. Filter on nonzero entries of the closure.
- [ ] **`trim` computes both `forward()` and `backward()`, each invoking `_lehmann`**: These share the same transitive closure `K`. Factor out `K` computation to avoid recomputing it.
- [ ] **Determinization creates `frozendict` states**: `semiring_wfsa.py:52` builds `frozendict` for each power-set state. For large nondeterministic automata this can blow up exponentially (inherent to subset construction, but consider adding a state-count limit with a clear error).

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

- [x] Remove unused imports: `defaultdict` and `Counter` in `field_wfsa.py:15`
- [ ] Remove dead commented-out code (e.g., the `__call__` override, `epsremove` override, `_hash` block in `Simple`)
- [ ] `base.py:109` raises `NotImplementedError` for `arcs(a=..., i=None)` — either implement or document why it's excluded
- [ ] Duplicated `push` implementation in `field_wfsa.py` and `semiring_wfsa.py` — factor into `base.py` (the code is identical)
- [ ] `WFSA.zero` and `WFSA.one` are set as class attributes by assignment after class definition (`field_wfsa.py:143-144`), overriding the `@property` in `base.py`. This is fragile — use `classproperty` or a `__init_subclass__` hook.
