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
    # Fallback to standard Gemini API if ADC is not found
    pass


def fetch_anomaly_data(source: str) -> str:
    """Fetches anomaly data from astronomical and particle physics sources.

    Args:
        source: The name of the data source (e.g., CERN, JWST, Vera C. Rubin)

    Returns:
        A string containing the latest anomaly data from the specified source.
    """
    source_lower = source.lower()
    if "cern" in source_lower:
        return "CERN Anomaly Data: B-meson decay anomalies detected. Potential lepton flavor universality violation."
    elif "jwst" in source_lower:
        return "JWST Anomaly Data: Unusually massive galaxies detected at very high redshifts (z > 10). Tensions with standard cosmology."
    elif "rubin" in source_lower or "vera" in source_lower:
        return "Vera C. Rubin Anomaly Data: High rate of unusual optical transients detected in recent deep drilling fields."
    else:
        return f"No anomaly data available for source: {source}"

def execute_push_tool(digest: str) -> str:
    """Executes the push tool to broadcast or store the formulated digest.

    Args:
        digest: The formulated digest text summarizing the anomalies.

    Returns:
        A success message indicating the digest was pushed.
    """
    return f"Successfully pushed the following digest to the central datastore: {digest}"


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI assistant designed to provide accurate and useful information. Use the tools provided to you to fetch anomaly data and execute the push tool when requested.",
    tools=[get_weather, get_current_time, fetch_anomaly_data, execute_push_tool],
)

app = App(
    root_agent=root_agent,
    name="app",
)
