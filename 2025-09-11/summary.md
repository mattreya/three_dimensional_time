# Summary for 2025-09-11: Euclid Data Investigation

## Goal

The primary objective for this session was to query the Euclid Science Archive to find and retrieve data on gravitational lensing candidates, specifically looking for anomalous shear values.

## Investigation Summary

Our initial approach was to use the ADQL query specified in the `ANALYSIS_PLAN.md` file. However, this failed because the target table, `euclid_dr1.lensing_catalog`, does not exist in the current data release.

This led to a systematic, multi-step investigation to locate the correct data:

1.  **Schema Exploration:** We successfully queried the `tap_schema.tables` to get a complete list of available tables in the database.
2.  **Table Inspection:** We then inspected the columns of the most promising tables:
    *   `catalogue.mer_catalogue`
    *   `catalogue.mer_morphology`
    *   `catalogue.spectro_zcatalog_spe_galaxy_candidates`
    None of these tables contained the required gravitational shear (`g1`, `g2`) data.
3.  **Final Attempt:** An attempt to inspect `catalogue.mer_final_catalogue` failed, suggesting the table is inaccessible or empty.
4.  **External Search:** We performed web searches to find official documentation. This led to broken links for the primary documentation (the DPDD) and a misleading link to a software package on Zenodo.

## Conclusion & Next Steps

We have concluded that the gravitational lensing data is not available in a simple, queryable table within the Euclid archive at this time. The data is likely part of a more complex data product that is not directly exposed via the TAP service, or it may be part of a future data release.

We also determined that calculating the shear values ourselves is not feasible due to the lack of essential Point Spread Function (PSF) correction data.

**Action Taken:**

*   A formal request has been sent to the Euclid helpdesk to ask for the correct table name, column names, and access method for the gravitational shear data.

**Next Step:**

*   We are now awaiting a response from the helpdesk. Once they provide the necessary information, we can resume our data mining efforts.
