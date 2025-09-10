



# src/euclid_data_miner.py
#
# This program queries the Euclid Science Archive for objects with anomalous
# gravitational lensing properties, based on the 3D time hypothesis.

# Before running, ensure you have astroquery installed:
# pip install astroquery

from astroquery.esa.euclid import Euclid

def find_lensing_anomalies():
    """
    Queries the Euclid Science Archive for anomalous lensing candidates.
    """
    print("Connecting to Euclid Science Archive...")

    # Note: Authentication may be required for full access.
    # You may need to register on the ESA Cosmos portal and use:
    # Euclid.login('your_username', 'your_password')

    # This ADQL query selects sources with high confidence and high shear values,
    # which could be candidates for our theory.
    # Query tap_schema.columns to get column names for catalogue.mer_catalogue
    adql_query = """
    SELECT
      column_name, data_type, description
    FROM
      tap_schema.columns
    WHERE
      table_name = 'catalogue.mer_catalogue'
    """

    print("Executing ADQL query to get column names...")
    print(f"Query: {adql_query}")

    try:
        job = Euclid.launch_job(adql_query)
        columns_table = job.get_results()

        if not columns_table:
            print("Could not retrieve column information for catalogue.mer_catalogue.")
            return

        print("Columns in catalogue.mer_catalogue:")
        for row in columns_table:
            print(f"- {row['column_name']} ({row['data_type']}): {row['description']}")

    except Exception as e:
        print(f"An error occurred during the query: {e}")
        print("This could be due to a connection issue, or the archive may not be available.")
        print("Please check your internet connection and the ESA/Euclid server status.")

    # Placeholder ADQL query - REPLACE WITH ACTUAL TABLE/COLUMN NAMES FROM EUCLID DOCS
    # adql_query = """
    # SELECT
    #   source_id, ra, dec, FLUX_VIS_nFWHM_APER, DET_QUALITY_FLAG
    # FROM
    #   catalogue.mer_catalogue
    # WHERE
    #   DET_QUALITY_FLAG = 0
    # """

    # print("Executing ADQL query...")
    # print(f"Query: {adql_query}")

    # try:
    #     job = Euclid.launch_job(adql_query)
    #     candidate_table = job.get_results()

    #     if not candidate_table:
    #         print("Query executed successfully, but no candidate objects were found.")
    #         return

    #     # Save the results to a local file
    #     output_file = "euclid_lensing_candidates.csv"
    #     candidate_table.write(output_file, format="csv", overwrite=True)
    #     print(f"Success! Found {len(candidate_table)} candidates. Saved to {output_file}")

    # except Exception as e:
    #     print(f"An error occurred during the query: {e}")
    #     print("This could be due to a connection issue, or the archive may not be available.")
    #     print("Please check your internet connection and the ESA/Euclid server status.")

if __name__ == "__main__":
    find_lensing_anomalies()
