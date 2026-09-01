# Repository Guidelines

## Project Structure & Module Organization

This is a Python 3.13 Anki add-on. Production code lives in
`src/anki_ai_workspace/`; `addon.py` registers the add-on, `reviewer.py`
integrates with Anki's reviewer, and `codex_client.py` bridges to the local
Codex CLI. Keep Anki-native integration in `ui/` and reviewer JavaScript in
`web/`. Unit and source-structure tests live in `tests/`. The packaged add-on
is written to `dist/anki_ai_workspace.ankiaddon`.

## Build, Test, and Development Commands

- `make install-dev` installs pinned development dependencies.
- `make format` formats `src/` and `tests/` with Black.
- `make lint` checks Black formatting without editing files.
- `make check` compiles Python sources to catch syntax errors.
- `make test` runs the `unittest` suite with `src/` on `PYTHONPATH`.
- `make build VERSION=0.1.0` creates the distributable archive.
- `make install VERSION=0.1.0` builds and installs locally; set
  `ANKI_ADDONS_DIR=/path/to/addons21` for a custom Anki location.

Run `make lint`, `make check`, and `make test` before review. Use
`make install-hooks` once to enable the repository hook.

## Coding Style & Naming Conventions

Use four-space Python indentation and Black's 88-character line length.
Follow existing `snake_case` module, function, variable, and test names;
use `PascalCase` for classes. Keep changes explicit and narrowly scoped rather
than introducing broad abstractions. Place new tests in `tests/test_<feature>.py`
and name test methods `test_<expected_behavior>`.

## Safety, Configuration, and Tests

Do not modify Anki scheduling, intervals, note fields, or card content. Treat
card/profile text as untrusted at every UI and prompt boundary, and never log
card text, prompts, replies, or credentials. Preserve the separation between
portable profile definitions and local deck assignments. Update tests and the
relevant README when behavior changes; update `src/anki_ai_workspace/README.md`
when add-on help text changes.

## Commits & Pull Requests

The available history currently contains the `v0.1.0` release commit, so there
is no established detailed commit convention. Use short, imperative subjects,
for example `Handle empty reviewer context`. Keep each pull request focused and
describe what changed, why, how it was tested, and any documentation,
configuration, or profile impact. Explain changes to protected release files
(`build.sh`, `install.sh`, `manifest.json`, `config.json`, changelog, or
workflows) and avoid unrelated edits to them.
