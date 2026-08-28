# The Three Dimensions of Time: A Gauge-Invariant Investigation

This project investigates the hypothesis of multi-dimensional time through the mathematical framework of **Two-Time (2T) Physics** (Itzhak Bars), **Superluminal $1+3$ Spacetime** (Dragan et al.), and the **Standard Model Extension (SME)** (Kostelecký).

---

## Core Hypothesis: The Gauge-Invariant Two-Tier Universe

1. **The Einstein Tier (Observable Spacetime):** Our standard $3+1$ Minkowski universe governed by Einstein's relativity, the second law of thermodynamics, and subluminal observer dynamics.
2. **The Quantum Tier (The Conformal Bulk):** A $4+2$ dimensional phase space $(X^M, P^M)$ subject to first-class $Sp(2, \mathbb{R})$ gauge constraints ($X^2=0, P^2=0, X\cdot P=0$). This eliminates unphysical negative-norm states (ghosts) while allowing conformal $SO(4,2)$ bulk symmetries to manifest holographically.

---

## Current Progress & Empirical Findings (August 27, 2026)

### 1. Full 5.13M LHCb Collision Dataset Analysis (`B2HHH_MagnetDown.root`)
* **Signal Candidates Isolated:** $373,696$ clean $B^\pm \to h^\pm h^+ h^-$ events across the Dalitz phase space ($m_B \in [5180, 5380]\text{ MeV}$).
* **Global Raw CP Asymmetry:** $A_{\text{CP}} = -0.00918 \pm 0.00164$.
* **Standard Model Extension (SME) Directional Differentials:** Evaluated forward-backward asymmetry differentials along laboratory axes across 4 Dalitz quadrants. Vertical ($P_y$) and longitudinal ($P_z$) boost differentials are consistent with zero ($< 2\sigma$).
* **Empirical Energy Scale Limit:** Established a **95% Confidence Level lower bound on the effective chiral/multi-temporal scale**:
  $$\mathbf{\Lambda \ge 90.88\text{ TeV}}$$

### 2. Corrected Euclid Galaxy Orientation Statistics (`euclid_lensing_candidates.csv`)
* **Axial Circular Statistics:** Corrected an earlier `arctan2` angle-modulo bug that created the artificial $57.56^\circ$ "Temporal Orthogonality" claim.
* **Empirical Nearest-Neighbor Difference:** **$44.59^\circ$** (consistent with the isotropic random expectation of $45.00^\circ$).

---

## Repository Structure

```
.
├── WHITE_PAPER.md                    # Formal scientific white paper
├── FORMULA.md                        # Mathematical derivations & EFT operators
├── README.md                         # Project overview and status
├── 2026-08-27/                       # Current session summary and milestone report
│   └── summary.md
├── src/
│   ├── lhcb_sme_dalitz_analysis.py   # Full 5.13M LHCb SME Dalitz analysis script
│   ├── corrected_multiscale_analysis.py # Multi-scale Euclid & LHCb validation
│   ├── analyze_alignment.py          # Legacy galaxy alignment tool
│   ├── detect_boundary_crossings.py  # Legacy boundary detection tool
│   └── euclid_data_miner.py          # ESA Euclid archive query tool
├── hossenfelder_sanity_model/        # 2T-Physics gauge constraint simulation suite
└── 2025-11-17_analysis/euclid_plots/ # Diagnostic plots & CSV outputs
```

---

## Running the Analyses

1. **Run Full LHCb Heavy Flavor SME Dalitz Analysis:**
   ```bash
   python src/lhcb_sme_dalitz_analysis.py
   ```

2. **Run Corrected Multi-Scale Alignment & Dalitz Validation:**
   ```bash
   python src/corrected_multiscale_analysis.py
   ```

3. **Run 2T-Physics Gauge Simulation:**
   ```bash
   python hossenfelder_sanity_model/lattice_predictor.py
   ```

---

## Dependencies
Requires `python >= 3.10`, `numpy`, `pandas`, `matplotlib`, `uproot`, `astropy`, and `scipy`.
```bash
pip install -r requirements.txt
```
