# The Three Dimensions of Time: A Gauge-Invariant Investigation

This project investigates the hypothesis of multi-dimensional time through the mathematical framework of **Two-Time (2T) Physics** (Itzhak Bars), **Superluminal $1+3$ Spacetime** (Dragan et al.), and the **Standard Model Extension (SME)** (Kostelecký).

---

## Core Hypothesis: The Gauge-Invariant Two-Tier Universe

1. **The Einstein Tier (Observable Spacetime):** Our standard $3+1$ Minkowski universe governed by Einstein's relativity, the second law of thermodynamics, and subluminal observer dynamics.
2. **The Quantum Tier (The Conformal Bulk):** A $4+2$ dimensional phase space $(X^M, P^M)$ subject to first-class $Sp(2, \mathbb{R})$ gauge constraints ($X^2=0, P^2=0, X\cdot P=0$). This eliminates unphysical negative-norm states (ghosts) while allowing conformal $SO(4,2)$ bulk symmetries to manifest holographically.

---

## Current Progress & Empirical Findings (October 17, 2026)

### 1. Looking From Quantum (3D Time) Into Classical (1D Time) Physics (`src/quantum_to_classical_3d_time_sim.py`)
* **Binary Wavefunction Collapse via Dimensional Reduction:** Prior to measurement, a quantum state evolves across a 3D temporal volume $(t_1, t_2, t_3)$ in the $(1+3)$ / $(4+2)$ bulk. Measurement by a classical $(3+1)$ apparatus gauge-fixes $t_2 = t_3 = 0$ on the measured subsystem, forcing its continuous superposition into a discrete **binary eigenvalue** ($\lambda \in \{+1, -1\}$) along the 1D classical timeline $t_1$.
* **Extra-Temporal Entanglement Bridge:** Subsystems that are **spacelike disconnected** in $(3+1)$ classical spacetime ($\Delta s_{3+1}^2 < 0$) remain **null-connected ($\Delta s_{\text{bulk}}^2 = 0$)** through the orthogonal temporal plane:
  $$c^2\left(\Delta t_2^2 + \Delta t_3^2\right) = |\Delta \vec{x}|^2 - c^2 \Delta t_1^2$$
* **15 $SO(4,2)$ Bulk Generators ($6$ Classical + $9$ Quantum):** Local collapse fixes the 6 classical Lorentz generators $L^{\mu\nu} \in SO(3,1)$, leaving the **9 extra-temporal bulk generators** ($L^{M4}, L^{M5}$) intact to carry non-local quantum mutual information ($2.0000\text{ bits}$) beyond $(3+1)$ spacetime without violating classical causality.
* **Empirical 3-Body LHCb Verification ($373,696$ Signal $B^\pm \to h_1^\pm h_2^+ h_3^-$ Events):**
  * **Binary Helicity Split:** The resonant $(h_1, h_2)$ pair bifurcates into binary helicity states $\cos\theta_{\text{hel}} \to +1$ ($64.82\%$) and $\cos\theta_{\text{hel}} \to -1$ ($35.18\%$).
  * **Quantum Mutual Information Excess:** Observed Dalitz mutual information $I_{\text{quantum}}(s_{12}; s_{23}) = \mathbf{0.4027\text{ bits}}$ vs. classical uncorrelated phase-space baseline $I_{\text{classical}} = \mathbf{0.0885\text{ bits}}$ (**$+0.3142\text{ bits}$ / $4.55\times$ quantum excess**).

![Quantum-to-Classical 3D Time Architecture](2026-10-17/quantum_to_classical_3d_time_architecture.png)

![CERN LHCb 3-Body Entanglement Bridge](2026-10-17/lhcb_3body_quantum_entanglement_bridge.png)

### 2. Full 5.13M LHCb Collision Dataset SME Analysis (`B2HHH_MagnetDown.root`)
* **Signal Candidates Isolated:** $373,696$ clean $B^\pm \to h^\pm h^+ h^-$ events across the Dalitz phase space ($m_B \in [5180, 5380]\text{ MeV}$).
* **Global Raw CP Asymmetry:** $A_{\text{CP}} = -0.00918 \pm 0.00164$.
* **Standard Model Extension (SME) Directional Differentials:** Evaluated forward-backward asymmetry differentials along laboratory axes across 4 Dalitz quadrants. Vertical ($P_y$) and longitudinal ($P_z$) boost differentials are consistent with zero ($< 2\sigma$).
* **Empirical Energy Scale Limit:** Established a **95% Confidence Level lower bound on the effective chiral/multi-temporal scale**:
  $$\mathbf{\Lambda \ge 90.88\text{ TeV}}$$

### 3. Corrected Euclid Galaxy Orientation Statistics (`euclid_lensing_candidates.csv`)
* **Axial Circular Statistics:** Corrected an earlier `arctan2` angle-modulo bug that created the artificial $57.56^\circ$ "Temporal Orthogonality" claim.
* **Empirical Nearest-Neighbor Difference:** **$44.59^\circ$** (consistent with the isotropic random expectation of $45.00^\circ$).

---

## Repository Structure

```
.
├── WHITE_PAPER.md                             # Formal scientific white paper
├── FORMULA.md                                 # Mathematical derivations & EFT operators
├── README.md                                  # Project overview and status
├── 2026-10-17/                                # Quantum-to-Classical 3D Time collapse & visuals
│   ├── summary.md
│   ├── quantum_to_classical_3d_time_architecture.png
│   └── lhcb_3body_quantum_entanglement_bridge.png
├── 2026-08-27/                                # LHCb SME Dalitz audit & milestone report
│   └── summary.md
├── src/
│   ├── quantum_to_classical_3d_time_sim.py    # 3D-Time binary collapse & LHCb entanglement simulator
│   ├── lhcb_sme_dalitz_analysis.py            # Full 5.13M LHCb SME Dalitz analysis script
│   ├── corrected_multiscale_analysis.py       # Multi-scale Euclid & LHCb validation
│   ├── analyze_alignment.py                   # Legacy galaxy alignment tool
│   ├── detect_boundary_crossings.py           # Legacy boundary detection tool
│   └── euclid_data_miner.py                   # ESA Euclid archive query tool
├── hossenfelder_sanity_model/                 # 2T-Physics gauge constraint simulation suite
└── 2025-11-17_analysis/euclid_plots/          # Diagnostic plots & CSV outputs
```

---

## Running the Analyses

1. **Run Quantum-to-Classical 3D Time Collapse & Entanglement Simulator:**
   ```bash
   python src/quantum_to_classical_3d_time_sim.py
   ```

2. **Run Full LHCb Heavy Flavor SME Dalitz Analysis:**
   ```bash
   python src/lhcb_sme_dalitz_analysis.py
   ```

3. **Run Corrected Multi-Scale Alignment & Dalitz Validation:**
   ```bash
   python src/corrected_multiscale_analysis.py
   ```

4. **Run 2T-Physics Gauge Simulation:**
   ```bash
   python hossenfelder_sanity_model/lattice_predictor.py
   ```

---

## Dependencies
Requires `python >= 3.10`, `numpy`, `pandas`, `matplotlib`, `uproot`, `astropy`, and `scipy`.
```bash
pip install -r requirements.txt
```
