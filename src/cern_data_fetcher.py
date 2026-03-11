import os
import sys
import subprocess
import requests

# Configuration
CERN_OPENDATA_RECORD_URL = "http://opendata.cern.ch/record/4900"
B2HHH_MAGNET_DOWN_URL = "http://opendata.cern.ch/record/4900/files/B2HHH_MagnetDown.root"
DOWNLOAD_DIR = "three_dimensional_time/data/cern_b_mesons"
MINER_SCRIPT_PATH = os.path.join(os.getcwd(), "three_dimensional_time/src/cern_data_miner.py")

def _download_latest_data():
    """
    Downloads the LHCb B-meson decay data.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    filename = B2HHH_MAGNET_DOWN_URL.split('/')[-1]
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    if os.path.exists(file_path):
        print(f"Data file already exists at {file_path}. Skipping download.")
        return file_path

    print(f"Downloading CERN Open Data from {B2HHH_MAGNET_DOWN_URL}")
    print(f"Saving to {file_path} (this is ~600MB and may take a few minutes)...")
    
    try:
        with requests.get(B2HHH_MAGNET_DOWN_URL, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Download complete.")
        return file_path
    except Exception as e:
        print(f"Failed to download data: {e}")
        return None

def run_cern_data_pipeline():
    """
    Checks for the CERN B-meson data, downloads it if missing,
    and runs the cern_data_miner.
    """
    print("Starting CERN B-meson data pipeline...")
    
    data_file = _download_latest_data()
    
    if data_file:
        data_file = os.path.abspath(data_file)
        print(f"Proceeding to mine data at: {data_file}")
        print(f"Running {MINER_SCRIPT_PATH}...")
        try:
            # Assumes running inside the .venv or a Python environment with uproot installed
            subprocess.run([sys.executable, MINER_SCRIPT_PATH, "--data_file", data_file], check=True, cwd=os.path.dirname(MINER_SCRIPT_PATH))
            print("CERN data miner executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running CERN data miner: {e}")
            print(f"Command: {e.cmd}")
            print(f"Stderr: {e.stderr}")
        except FileNotFoundError:
            print(f"Error: Miner script not found at {MINER_SCRIPT_PATH}. Please check the path.")
    else:
        print("Data file is missing or download failed. Pipeline aborted.")

if __name__ == '__main__':
    run_cern_data_pipeline()

