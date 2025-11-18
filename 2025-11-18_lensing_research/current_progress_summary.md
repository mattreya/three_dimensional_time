# Current Progress Summary (2025-11-18)

This document summarizes our ongoing investigation into the hypothesis of "dimensional lensing" and "orthogonal galaxies."

## 1. Hypothesis Under Investigation

- **Core Idea:** We are exploring the hypothesis that massive, unobservable objects (e.g., dark matter concentrations) could be acting as "dimensional lenses." These lenses might "fold" or "warp" spacetime in a way that allows us to peer into orthogonal dimensions, making galaxies from those dimensions ("orthogonal galaxies") visible to us.
- **Expected Evidence:** If this hypothesis holds, we would expect to find signs of strong gravitational lensing (arcs, rings, multiple images) around our anomalous galaxy candidates, indicating the presence of such a massive lensing object.

## 2. Candidate Galaxies

We are focusing on two extreme ellipticity candidates identified from the `2025-09-17` analysis:

-   **High Ellipticity ("Needle"):** An object in the constellation **Horologium**.
    -   Coordinates: RA=58.37, Dec=-47.79
    -   Image File: `three_dimensional_time/2025-09-17/lensing_search/Horologium_candidate.png`
    -   FITS Data: `three_dimensional_time/2025-09-17/lensing_search/Horologium_candidate.fits`

-   **Low Ellipticity ("Circle"):** An object in the constellation **Draco**.
    -   Coordinates: RA=275.14, Dec=64.97
    -   Image File: `three_dimensional_time/2025-09-17/lensing_search/Draco_candidate.png`
    -   FITS Data: `three_dimensional_time/2025-09-17/lensing_search/Draco_candidate.fits`

## 3. Reference Material

To aid in identifying lensing patterns, we have gathered examples of famous gravitational lensing events. These sources are summarized in:
- `three_dimensional_time/2025-11-18_lensing_research/lensing_examples.md`

## 4. Current Status: Computational Analysis Pending

-   **Objective:** To logically compare our candidate images with known gravitational lensing patterns.
-   **Method:** A Python script (`three_dimensional_time/src/analyze_lensing_images.py`) has been developed to perform a computational analysis of the FITS data. This script aims to detect sources and identify patterns (like arcs or multiple images) consistent with gravitational lensing.
-   **Dependency Resolved:** The `photutils` library, a dependency for the analysis script, has been successfully installed.
-   **Next Action:** The analysis script needs to be re-executed to generate the findings.
