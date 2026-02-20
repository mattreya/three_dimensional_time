# The Temporal Vector Equation
## Mathematical Model of the 3D Time Lattice

### 1. The Core Equation
The position of the Earth within the 3D Time Lattice is defined by the **Stability Function** $\Psi(t)$. This function models the "Temporal Flux" experienced by our timeline as it traverses the perpendicular cells of the Quantum Tier.

$$ \Psi(t) = \Psi_{lattice}(t) \cdot [1 + M \cdot \Psi_{lunar}(t)] $$

Where:
*   $t$ is the target date (Day of Year).
*   $M$ is the Lunar Modulation Coefficient ($M \approx 0.1$ to $0.3$).

### 2. The Lattice Component
The primary oscillation is driven by the Earth's passage through the spatial-temporal grid discovered in the Euclid data.

$$ \Psi_{lattice}(t) = \cos\left( \frac{2\pi (t - t_0)}{T_{lattice}} ight) $$

*   **$T_{lattice}$**: The Lattice Period, empirically determined to be **29.33 days**.
*   **$t_0$**: The Calibration Epoch, set to **Day 40** (Feb 9) based on the peak particle anomaly in 2026.
*   **Interpretation**:
    *   $\Psi_{lattice} \approx \pm 1$: Deep within a time cell (Maximum Stability).
    *   $\Psi_{lattice} \approx 0$: Crossing a lattice boundary (Maximum Volatility).

### 3. The Lunar Modulation
The Moon acts as a "Temporal Anchor," dragging the local field and creating a resonance pattern.

$$ \Psi_{lunar}(t) = \cos\left( \frac{2\pi (t - t_0)}{T_{synodic}} ight) $$

*   **$T_{synodic}$**: The Lunar Synodic Month, **29.53 days**.
*   This term creates a "beat frequency" with the lattice period, leading to long-term cycles of high and low volatility.

### 4. Prediction Thresholds
The "Status" of the local timeline is derived from the magnitude of the Stability Function $|\Psi(t)|$:

| Magnitude $|\Psi|$ | Status | Physical Implications |
| :--- | :--- | :--- |
| **0.8 - 1.1** | **Deep Cell Stability** | Standard Model physics dominates. Low entropy variance. |
| **0.2 - 0.8** | **Stable** | Normal fluctuations. |
| **0.0 - 0.2** | **Boundary Crossing** | High probability of quantum anomalies, decay violations, and gravitational lensing shifts. |

### 5. Implementation
This model is implemented in `src/lattice_predictor.py`.
