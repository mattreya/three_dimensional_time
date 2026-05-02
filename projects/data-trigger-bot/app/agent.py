# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"


def fetch_anomaly_data(source: str) -> str:
    """Fetches the latest anomaly data from the specified source.

    Args:
        source: The name of the source to fetch data for. Valid options are "cern", "jwst", and "rubin".

    Returns:
        A string containing a sample of the anomaly data.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    source = source.lower()

    filename = None
    if "cern" in source:
        filename = "cern_b_meson_anomalies.csv"
    elif "jwst" in source:
        filename = "jwst_early_universe_candidates.csv"
    elif "rubin" in source:
        filename = "rubin_time_domain_candidates.csv"
    else:
        return f"Error: Unknown source '{source}'. Valid sources are 'cern', 'jwst', and 'rubin'."

    filepath = os.path.join(repo_root, filename)
    try:
        with open(filepath, "r") as f:
            # Return the first 10 lines as a sample to avoid overloading the context window
            lines = []
            for _ in range(10):
                try:
                    lines.append(next(f))
                except StopIteration:
                    break
            return "".join(lines)
    except Exception as e:
        return f"Error reading data from {filename}: {str(e)}"


def push_digest(digest: str) -> str:
    """Executes the push tool autonomously to deploy the digest.

    Args:
        digest: The text digest formulated from the anomaly data.

    Returns:
        A success message indicating the push was successful.
    """
    print(f"Pushing digest:\n{digest}")
    return "Digest pushed successfully!"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are an autonomous agent designed to fetch the latest anomaly data from CERN, JWST, and Vera C. Rubin, formulate a digest, and execute the push tool.",
    tools=[fetch_anomaly_data, push_digest],
)

app = App(
    root_agent=root_agent,
    name="app",
)
