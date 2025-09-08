# Python-Based Remote Analysis Plan

This document outlines the strategy for using Python to remotely query and filter data from the Euclid and Rubin observatories, avoiding the need for large local data storage.

## 1. Euclid Mission Data Analysis

**Tool:** The `astroquery` Python library.

**Workflow:**
1.  Install the library: `pip install astroquery`
2.  In a Python script, import the necessary modules.
3.  Authenticate to the Euclid Science Archive (this will likely require credentials from the ESA Cosmos portal).
4.  Construct a query in ADQL to select only galaxies that meet specific criteria for being anomalous (e.g., high gravitational shear, unusual morphology flags).
5.  Execute the query using `astroquery`.
6.  The result will be an `astropy.table.Table` object containing only the candidate objects. This table can be saved locally.

**Example Code Snippet:**

```python
from astroquery.euclid import Euclid

# Authenticate (specifics may vary)
# Euclid.login('your_username', 'your_password')

# Construct ADQL query to find objects with unusual lensing properties
adql_query = """
SELECT
  source_id, ra, dec, shear_g1, shear_g2
FROM
  euclid_dr1.lensing_catalog
WHERE
  shear_confidence > 0.8 AND (ABS(shear_g1) > 0.5 OR ABS(shear_g2) > 0.5)
"""

# Execute the query
print("Executing query on Euclid archive...")
candidate_table = Euclid.query_system_main(adql_query)

# Save the small results table
if candidate_table:
  candidate_table.write("euclid_candidates.csv", format="csv", overwrite=True)
  print(f"Found {len(candidate_table)} candidates. Saved to euclid_candidates.csv")

```

## 2. Vera C. Rubin Observatory Data Analysis

**Tool:** The Rubin Science Platform (RSP) Notebook environment.

**Workflow:**
1.  Log into the RSP via your web browser.
2.  Launch a new JupyterLab notebook.
3.  Use the provided LSST Science Pipelines libraries (e.g., the "Butler" data access tool) to interface with the database.
4.  Construct a query to filter the object catalog based on your criteria (e.g., anomalous colors, rapid variability, unusual shape parameters).
5.  The query results are loaded into your notebook as a Pandas DataFrame or similar object.
6.  Perform any further analysis or visualization in the notebook.
7.  Save the final, small candidate list and download it from the RSP interface to your local machine.

**Conceptual Example (syntax will vary based on final LSST libraries):**

```python
# This code runs inside the Rubin Science Platform Notebook
from lsst.rsp import get_dataset

# The Butler is the tool for data access
butler = get_dataset("lsst_dr1")

# Define a query for unusual objects
sql_query = """
SELECT
  objectId, ra, dec, u_mag, g_mag, r_mag, i_mag
FROM
  object_catalog
WHERE
  is_variable = 1 AND (u_mag - g_mag) < -0.4 -- Example: very blue variable objects
"""

# Retrieve the data
candidates_df = butler.query(sql_query).to_pandas()

# Save the results within the RSP environment
candidates_df.to_csv("rubin_candidates.csv")

print(f"Found {len(candidates_df)} candidates. Saved to rubin_candidates.csv")
# You can then download this file from the Jupyter interface.
```
