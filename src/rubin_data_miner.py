# src/rubin_data_miner.py
#
# CONCEPTUAL TEMPLATE
# This program is designed to be run within the Rubin Science Platform (RSP)
# notebook environment. It will not run locally.

# The RSP provides custom libraries, like 'lsst.rsp', for data access.

from lsst.rsp import get_dataset
import pandas as pd

def find_anomalous_variability():
    """
    Queries the LSST database for objects with unusual variability or color,
    which could be clues for non-standard cosmological phenomena.
    """
    print("Connecting to the LSST database via the Butler...")

    try:
        # The 'Butler' is the main tool for data access within the RSP
        butler = get_dataset("lsst_dr1") # The dataset name may change

        # This query looks for objects that are highly variable and have very blue colors,
        # a potential signature of an unusual energy event.
        sql_query = """
        SELECT
          objectId, ra, dec, u_mag, g_mag, r_mag, i_mag, is_variable
        FROM
          object_catalog
        WHERE
          is_variable = 1 AND (u_mag - g_mag) < -0.4
        """

        print("Executing SQL query...")
        print(f"Query: {sql_query}")

        # The query method returns the data, which we can convert to a Pandas DataFrame
        candidates_df = butler.query(sql_query).to_pandas()

        if candidates_df.empty:
            print("Query executed successfully, but no candidate objects were found.")
            return

        # Save the results within the RSP's file system
        output_file = "rubin_variability_candidates.csv"
        candidates_df.to_csv(output_file)

        print(f"Success! Found {len(candidates_df)} candidates. Saved to {output_file}")
        print("You can download this file from the JupyterLab interface in the RSP.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("This script must be run inside the Rubin Science Platform.")

if __name__ == "__main__":
    find_anomalous_variability()
