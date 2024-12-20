# Fireflies CLI

Command line interface for Fireflies.ai. This package provides a convenient way to interact with Fireflies.ai from the command line.

## Installation

```bash
pip install fireflies-cli
```

## Usage

```bash
# Set your API key (only needed once)
ff config set-key YOUR_API_KEY

# Join a meeting
ff join --url https://meet.google.com/xxx-yyyy-zzz

# Get video URL for a transcript
ff video TRANSCRIPT_ID

# Download video
ff video -d TRANSCRIPT_ID

# List recent transcripts
ff list

# Delete a transcript
ff delete TRANSCRIPT_ID
```

## Features

- Join meetings with optional duration and name
- Get video URLs for transcripts
- Download meeting recordings
- List transcripts
- Delete transcripts

## Note

This CLI tool uses the `fireflies-sdk` package. If you need programmatic access to Fireflies.ai, consider using the SDK directly.
