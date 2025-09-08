# The Three Dimensions of Time: A Data-Driven Investigation

This project is a speculative research effort to find evidence for the hypothesis that time, like space, is not a single dimension but has a more complex, multi-dimensional structure.

## Core Hypothesis: The Two-Tier Universe

Our working theory posits a "Two-Tier" model of the universe:

1.  **The Einstein Tier (1-3% of Reality):** The observable universe we live in. It is governed by the 2nd Law of Thermodynamics and Einstein's theory of relativity, where the speed of light is a constant.

2.  **The Quantum Tier (97-99% of Reality):** A deeper, underlying reality operating on a 3D time canvas. This tier is not bound by the 2nd Law or the speed of light, allowing for non-local events and entropy reversals.

This project seeks to find "leaked clues" from the Quantum Tier as they manifest in our own.

## Project Goal

The goal of this project is to identify, retrieve, and analyze data from major astronomical observatories to find anomalies that could be interpreted as evidence for the Two-Tier Universe hypothesis.

## Methodology

Our strategy is to perform a remote analysis of large astronomical datasets, focusing on three primary clues:

1.  **Gravitational Anomalies:** Searching for unusual gravitational lensing effects that could be attributed to "dark matter" being ordinary matter existing off-axis in the time canvas.
2.  **Non-Local Events:** Analyzing quantum entanglement data to find correlations with gravitational fields, suggesting a link through the Quantum Tier.
3.  **Cosmological Evolution Anomalies:** Searching for objects in the early universe (via JWST) that are "too ordered, too soon," which would imply a loophole in the 2nd Law of Thermodynamics.

Due to the massive size of the datasets, our approach is to use Python libraries to query and filter data on the observatories' servers, downloading only small, manageable lists of candidate objects.

## Repository Structure

```
.
├── README.md                 # This file
├── TASKS.md                  # High-level project tasks for data collection
├── ANALYSIS_PLAN.md          # Detailed technical plan for remote Python-based analysis
├── .gitignore                # Excludes virtual environments and IDE files
├── 2025-09-08/
│   └── summary.md            # Summary of the initial brainstorming session
└── src/
    ├── euclid_data_miner.py    # Script to query the ESA Euclid Science Archive
    └── rubin_data_miner.py     # Conceptual template for the Rubin Science Platform
```

## Getting Started

1.  **Understand the Plan:** Read the `ANALYSIS_PLAN.md` file for a detailed overview of the technical strategy.

2.  **Install Dependencies:** The primary local script requires the `astroquery` library.
    ```bash
    pip install astroquery
    ```

3.  **Run the Euclid Miner:** Execute the script to begin searching for lensing candidates in the Euclid data archive.
    ```bash
    python src/euclid_data_miner.py
    ```
