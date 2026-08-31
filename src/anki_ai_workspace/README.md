# Anki AI Workspace

Anki AI Workspace adds an AI workspace to Anki's review screen. It can answer
questions about the card currently on screen and provide reusable, deck-specific
actions through profiles.

## Before you begin

The current release uses the Codex CLI. Install it and sign in; the add-on uses
that saved CLI session and does not require an API key.

Follow the official Codex installation and sign-in instructions, then run
`codex` in a terminal if setup has not already been completed.

Restart Anki, open a review card, and choose the sparkle button. The first chat
checks that Codex is available before sending a request.

## Use profiles

Create profiles and bind them to decks from **Tools → AI Deck Profiles…**.
A subdeck inherits its nearest parent profile unless it has a direct assignment.
Profiles can be exported and shared; local deck assignments are never exported.

Choose a profile action to send its instruction immediately, or choose
**Custom chat** to type a question. Each card keeps a separate, temporary
conversation while Anki is running. Use the conversation menu in the chat title
bar to switch between active card conversations.

## Privacy and troubleshooting

Each request runs in a temporary, read-only directory and is discarded after it
finishes. The add-on's operational log never includes card text, profile text,
prompts, chat messages, credentials, or Codex output.

If the connection check fails, first confirm `codex --version` works in a new
terminal, then run `codex` again to complete sign-in. Restart Anki after either
step and use **Retry connection** in the chat window.

For configuration details, see `config.md` in this add-on folder.
