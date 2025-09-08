# Project Tasks: Data Collection & Retrieval

This document outlines the initial tasks for collecting the data needed to search for the "leaked clues" of 3D time.

### Category 1: Gravitational Anomaly Search (Dark Matter & Lensing)

- [ ] **Task 1.1:** Identify and bookmark the public data access portals for the ESA Euclid mission and the Vera C. Rubin Observatory.
- [ ] **Task 1.2:** Research the specific data products related to weak gravitational lensing, galaxy shear catalogs, and photometric redshift data.
- [ ] **Task 1.3:** Write initial Python scripts using `astropy` and `requests`/`astroquery` to perform test queries against the relevant data archives.
- [ ] **Task 1.4:** Plan local storage strategy. Estimate storage needs for sample datasets (start with a 10-20 TB projection).

### Category 2: Non-Local Search (Quantum Entanglement)

- [ ] **Task 2.1:** Locate and register for access to the CERN Open Data portal and the Fermilab Public Dataset portal.
- [ ] **Task 2.2:** Search for documentation or publications regarding the data release policy for the Micius quantum satellite experiments.
- [ ] **Task 2.3:** Draft a formal data request proposal template that can be submitted to research groups if their data is not publicly available.
- [ ] **Task 2.4:** Investigate and install Python libraries (e.g., `uproot` for CERN data) capable of reading and parsing common high-energy physics data formats.

### Category 3: Cosmic Evolution Search (JWST & Early Universe)

- [ ] **Task 3.1:** Create a user account on the STScI MAST (Mikulski Archive for Space Telescopes) portal.
- [ ] **Task 3.2:** Use the MAST portal to identify and list the program IDs for all major JWST deep field surveys (e.g., JADES, CEERS, GLASS).
- [ ] **Task 3.3:** Write a Python script using the `astroquery.mast` module to programmatically search for and filter data from these programs.
- [ ] **Task 3.4:** Implement and test a download function in the script to retrieve a small set of FITS image files from one of the deep fields as a proof-of-concept.
