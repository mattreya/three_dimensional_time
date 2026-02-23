import os
import sys
import subprocess
import datetime
import pandas as pd
import numpy as np
import requests

# Configuration
LHCb_GITHUB_REPO_URL = "https://github.com/cernopendata/LHCb-analysis-framework"
DOWNLOAD_DIR = "three_dimensional_time/data/cern_b_mesons"
MINER_SCRIPT_PATH = os.path.join(os.getcwd(), "three_dimensional_time/src/cern_data_miner.py")
LAST_UPDATE_FILE = os.path.join(DOWNLOAD_DIR, ".last_update_check")

def _get_latest_github_commit_hash(repo_url):
    """Fetches the latest commit hash from the main branch of a GitHub repository."""
    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/") + "/commits/main"
    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()['sha']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GitHub commit hash: {e}")
        return None

def _check_for_new_data():
    """
    Checks for new data by comparing the latest GitHub commit hash with a locally stored one.
    """
    latest_hash = _get_latest_github_commit_hash(LHCb_GITHUB_REPO_URL)
    if not latest_hash:
        print("Could not retrieve latest GitHub hash. Assuming no new data for now.")
        return False

    if not os.path.exists(LAST_UPDATE_FILE):
        print("First run: no previous update record found.")
        with open(LAST_UPDATE_FILE, 'w') as f:
            f.write(latest_hash)
        return True # Treat first run as new data to trigger initial processing

    with open(LAST_UPDATE_FILE, 'r') as f:
        previous_hash = f.read().strip()

    if latest_hash != previous_hash:
        print(f"New data detected! GitHub repo updated (from {previous_hash[:7]} to {latest_hash[:7]}).")
        with open(LAST_UPDATE_FILE, 'w') as f:
            f.write(latest_hash)
        return True
    else:
        print("No new data detected. GitHub repo is up to date.")
        return False

def _download_latest_data():
    """
    Placeholder: In a real scenario, this would download the latest relevant
    B-meson data file from the identified source. For now, it creates a dummy CSV.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dummy_data_filename = f"b_meson_data_{timestamp}.csv"
    dummy_data_path = os.path.join(DOWNLOAD_DIR, dummy_data_filename)

    print(f"Simulating download: Creating dummy data file at {dummy_data_path}")
    
    # Generate some dummy data that looks like B-meson CP asymmetry
    np.random.seed(int(datetime.datetime.now().timestamp())) # Seed based on current time
    n_days = 365
    days = np.arange(1, n_days + 1)
    
    # Introduce a slight periodic signal to make it interesting
    base_asymmetry = np.random.normal(loc=0.015, scale=0.002, size=n_days)
    periodic_signal = 0.003 * np.sin(2 * np.pi * days / (365/2)) # Twice a year
    cp_asymmetry_avg = base_asymmetry + periodic_signal

    df_dummy = pd.DataFrame({
        'day_of_year': days,
        'cp_asymmetry_avg': cp_asymmetry_avg
    })
    df_dummy.to_csv(dummy_data_path, index=False)
    print("Dummy data created.")
    return dummy_data_path

def run_cern_data_pipeline():
    """
    Checks for new CERN B-meson data, downloads it if available,
    and runs the cern_data_miner.
    """
    print("Starting CERN B-meson data pipeline...")
    if _check_for_new_data():
        latest_data_file = _download_latest_data()
        if latest_data_file:
            print(f"New data downloaded to: {latest_data_file}")
            # Run the miner script with the new data
            print(f"Running {MINER_SCRIPT_PATH} with new data...")
            try:
                # Assuming Python 3 for consistency
                # Ensure the miner script is executable or called directly with python
                subprocess.run([sys.executable, MINER_SCRIPT_PATH, "--data_file", latest_data_file], check=True, cwd=os.path.dirname(MINER_SCRIPT_PATH))
                print("CERN data miner executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error running CERN data miner: {e}")
                print(f"Command: {e.cmd}")
                print(f"Stderr: {e.stderr}")
            except FileNotFoundError:
                print(f"Error: Miner script not found at {MINER_SCRIPT_PATH}. Please check the path.")
        else:
            print("No data file was generated/downloaded.")
    else:
        print("No new B-meson data found at this time.")
    print("CERN B-meson data pipeline finished.")

if __name__ == '__main__':
    run_cern_data_pipeline()
