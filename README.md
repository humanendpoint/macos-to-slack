
## macOS release announce to Slack

This takes info from https://sofafeed.macadmins.io and whenever a new build is released (or whenever this runs) outputs the latest macOS version info to Slack.

### You'll need

- Somewhere to host this that accepts incoming requests (like a Google Cloud Run Function)
- A way to trigger (like a pub/sub topic)
- Some environment variables set:
  - `macosversion`
    - used to keep track of the **current** macOS version
  - `SLACK_TOKEN`
  - `CHANNEL_ID`

### Output

<img width="597" alt="Screenshot 2024-10-23 at 19 29 19" src="https://github.com/user-attachments/assets/2a06a5ad-34f4-4b00-897d-070e02c4a08f">
