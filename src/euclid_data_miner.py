# src/euclid_data_miner.py
#
# This program queries the Euclid Science Archive for objects with anomalous
# gravitational lensing properties, based on the 3D time hypothesis.

# Before running, ensure you have astroquery installed:
# pip install astroquery

from astroquery.euclid import Euclid

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
    adql_query = """
    SELECT
      source_id, ra, dec, shear_g1, shear_g2, snr
    FROM
      euclid_dr1.lensing_catalog
    WHERE
      snr > 10 AND (ABS(shear_g1) > 0.5 OR ABS(shear_g2) > 0.5)
    """

    print("Executing ADQL query...")
    print(f"Query: {adql_query}")

    try:
        candidate_table = Euclid.query_system_main(adql_query)

        if not candidate_table:
            print("Query executed successfully, but no candidate objects were found.")
            return

        # Save the results to a local file
        output_file = "euclid_lensing_candidates.csv"
        candidate_table.write(output_file, format="csv", overwrite=True)
        print(f"Success! Found {len(candidate_table)} candidates. Saved to {output_file}")

    except Exception as e:
        print(f"An error occurred during the query: {e}")
        print("This could be due to a connection issue, or the archive may not be available.")
        print("Please check your internet connection and the ESA/Euclid server status.")

if __name__ == "__main__":
    find_lensing_anomalies()
