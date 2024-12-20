# Fireflies Assistant

A command-line interface for Fireflies.ai to manage meeting transcripts and participants.

## Installation

```bash
pip install -e .
```

## Usage

First, set your Fireflies.ai API key:
```bash
ff key YOUR_API_KEY
```

### Commands

- Join a meeting (120 minutes duration):
  ```bash
  ff join
  ```

- List recent meetings:
  ```bash
  ff list
  ff list --limit 20  # Show more meetings
  ```

- Get transcript ID for a meeting URL:
  ```bash
  ff id "https://meet.google.com/abc-def-ghi"
  ```

- Get meeting participants:
  ```bash
  ff participants TRANSCRIPT_ID
  # or use meeting URL
  ff participants "https://meet.google.com/abc-def-ghi"
  ```

- Get meeting transcript:
  ```bash
  ff transcript TRANSCRIPT_ID
  # or use meeting URL
  ff transcript "https://meet.google.com/abc-def-ghi"
  ```

### Data Storage

- API key is stored in `.env` file
- Meeting URL to transcript ID mappings are stored in `~/.fireflies_meetings.json`

## Development

This project uses:
- Click for CLI interface
- python-dotenv for environment management
- requests for API communication
