# Autonomous Data Trigger Bot Walkthrough - April 25, 2026

## Overview
We built an autonomous data trigger bot designed to automatically monitor and evaluate anomalous astrophysical and particle physics data using the `google/agents-cli` framework.

## Project Structure
- Bootstrapped using Google's Agent Development Kit (ADK) leveraging Gemini Flash.
- Project location: `projects/data-trigger-bot/` (scaffolded via `agents-cli scaffold create --prototype`).

## Core Logic Implementation
- Replaced default app templates in `app/agent.py` to implement a custom persona.
- The prompt instructs the agent to focus on evaluating CERN B-meson anomalies, JWST early universe thermodynamics, and Vera C. Rubin dark matter/anomaly surveys.
- Supplied the agent with a custom Python tool: `update_unread_summary_and_push(content)`.
- Upon evaluation, the agent automatically executes this tool, which uses Python's `subprocess` module to generate an `UNREAD_summary.md` digest and automatically pushes the new commit directly to the repository.

## Automated Execution (GitHub Actions)
- The pipeline execution is automated using GitHub Actions within `.github/workflows/data_trigger.yml`.
- Runs on a daily cron schedule (`0 8 * * *`), triggering the bot at 8:00 AM UTC.
- The workflow establishes the required environment (`uv` and `google-agents-cli`) and injects the `GCP_PROJECT_ID` and `GEMINI_API_KEY` secrets.
- It then invokes `agents-cli run` with instructions to fetch the latest anomaly data, formulate a digest, and execute the push tool autonomously.

## Expected Loop
Every morning, the remote runner wakes up and processes new telemetry. Afterwards, you only need to sync your workspace to read the latest `UNREAD_summary.md` containing any detected anomalies.
