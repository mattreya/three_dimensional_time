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

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

import os
import google.auth

try:
    _, project_id = google.auth.default()
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"
except google.auth.exceptions.DefaultCredentialsError:
    pass


def fetch_cern_data(query: str) -> str:
    """Fetches the latest anomaly data from CERN.

    Args:
        query: Specific experiment or data type to query.

    Returns:
        A string containing the latest CERN anomaly data.
    """
    return "CERN Data: No new anomalies detected in LHC Run 3 data."


def fetch_jwst_data(query: str) -> str:
    """Fetches the latest anomaly data from JWST.

    Args:
        query: Specific celestial object or region to query.

    Returns:
        A string containing the latest JWST anomaly data.
    """
    return "JWST Data: Unexplained infrared signature detected near exoplanet K2-18b."


def fetch_vera_rubin_data(query: str) -> str:
    """Fetches the latest anomaly data from the Vera C. Rubin Observatory.

    Args:
        query: Specific sector or transient event type to query.

    Returns:
        A string containing the latest Vera Rubin anomaly data.
    """
    return "Vera Rubin Data: High-velocity transient object observed in Sector 42."


def push_digest(digest: str) -> str:
    """Pushes the formulated digest to the downstream systems.

    Args:
        digest: The text digest of the latest anomaly data.

    Returns:
        A string confirming the push status.
    """
    return "Digest successfully pushed to downstream channels."


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are an autonomous data trigger bot responsible for analyzing astrophysical and particle physics anomalies. Fetch the latest data from CERN, JWST, and Vera C. Rubin, formulate a digest, and push it using the available tools.",
    tools=[fetch_cern_data, fetch_jwst_data, fetch_vera_rubin_data, push_digest],
)

app = App(
    root_agent=root_agent,
    name="app",
)
