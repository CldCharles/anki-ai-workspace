# Anki AI Workspace

Anki AI Workspace is an Anki add-on that adds an AI workspace to the review
screen. Select an action or ask a question to get help with the card currently
being reviewed, without leaving Anki.

The current release connects through a locally authenticated Codex CLI session.
It does not require or store an API key.

## What it does

- Adds a chat launcher to every review card.
- Sends readable card fields as context for the selected card.
- Lets you define reusable actions and assign them to decks with profiles.
- Keeps separate temporary conversations for the cards you visit during an
  Anki session.
- Inherits a profile from a parent deck when a subdeck has no direct profile.

## Requirements

- Anki with add-on support.
- The Codex CLI installed and signed in.

## Install the add-on

### From a release file

1. Download `anki_ai_workspace.ankiaddon` from this project's release assets.
2. In Anki, choose **File → Import** and select the downloaded file.
3. Restart Anki when prompted.

### From a source checkout

```bash
git clone https://github.com/lmallez/anki-ai-workspace.git
cd anki-ai-workspace
make install VERSION=0.1.0
```

`make install` builds the add-on and installs it into the Anki profile found on
your system. If Anki is installed in a non-standard location, provide its
add-ons folder explicitly:

```bash
ANKI_ADDONS_DIR="/path/to/Anki2/addons21" make install VERSION=0.1.0
```

Restart Anki after installation or upgrade.

## Set up Codex

Install Codex using its official documentation, then run:

```bash
codex
```

After completing sign-in, start Anki. The workspace checks the connection when
you first open a chat. It uses `codex` from your PATH by default. If you need a
specific executable, change `codex_executable` in the add-on configuration to
its full path.

No API key is needed. Do not add one to the add-on configuration.

## Use

1. Review any card and select the sparkle button.
2. Choose a profile action, or choose **Custom chat** to type a question.
3. Open **Tools → AI Deck Profiles…** to create profiles and assign them
   to decks.

Profile exports contain profile definitions only; deck assignments remain local
to the Anki installation.

## Privacy and behavior

Each request runs through the locally authenticated Codex CLI in a temporary,
read-only working directory. It is discarded after the request completes. The
add-on keeps conversations only in memory for the active Anki session.

Its operational log deliberately omits card text, profile text, prompts, chat
messages, credentials, and raw Codex output. The log records only technical
status and size information useful for troubleshooting.

## Troubleshooting

- **Codex CLI was not found:** confirm that `codex --version` works in a new
  terminal, then restart Anki. If it does not, install Codex again using the
  official guide.
- **Codex is not signed in:** run `codex` in a terminal and complete its
  sign-in flow.
- **A request is taking too long:** use **Cancel** in the chat window, then try
  again. The default response timeout is 90 seconds.
- **Anki lives in a custom location:** set `ANKI_ADDONS_DIR` when installing
  from source, as shown above.

## Development

Requires Python 3.13.

```bash
make install-dev
make install-hooks
make lint
make check
make test
make build VERSION=0.1.0
```

The archive is written to `dist/anki_ai_workspace.ankiaddon`.

For the detailed configuration reference, see
[src/anki_ai_workspace/config.md](src/anki_ai_workspace/config.md).

## Repository structure

The repository uses the same lightweight `src/<package>` layout as the related
Anki Slot Machine project:

- `src/anki_ai_workspace/addon.py` registers the add-on and its Tools menu.
- `src/anki_ai_workspace/reviewer.py` connects the workspace to Anki Reviewer.
- `src/anki_ai_workspace/codex_client.py` contains the current Codex CLI bridge.
- `src/anki_ai_workspace/profiles.py` stores portable profiles and local deck assignments.
- `src/anki_ai_workspace/ui/` contains the Anki-native runtime integration.
- `src/anki_ai_workspace/web/` contains the persistent reviewer bridge.
- `tests/` contains the unit and source-structure test suite.

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Releases

Pushing a version tag (`v0.1.0`, for example) runs formatting, compilation, and
unit tests, then creates a GitHub Release containing the `.ankiaddon` archive.
Publishing to AnkiWeb is intentionally a separate manual step, so a maintainer
can use the appropriate AnkiWeb account without storing personal publishing
details in this repository.
