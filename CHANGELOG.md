# Changelog

## Unreleased

- Added optional profile-action shortcuts that run directly from review cards.
- Refined card shortcuts into a compact dark toolbar and kept profile management
  available from the action menu even when a profile is assigned.
- Reworked the profile editor with stable sections, aligned controls, and
  responsive form rows that avoid overlap at larger font and display scales.
- Reserved a dedicated grid row for the review-card shortcut option so the
  instruction editor cannot overlap it when the dialog is compressed.
- Made the profile editor vertically scrollable while keeping profile selection
  and dialog actions visible.
- Included the persistent `user_files` directory in release archives so Anki
  preserves profiles and local deck assignments during upgrades.

## 0.1.0 - 2026-08-31

- Added the initial Anki AI Workspace add-on, deck profiles, reviewer workspace,
  Codex CLI integration, packaging, and release automation.
- Added contributor guidance, code ownership, and the same opt-in pre-commit
  formatting hook used by Anki Slot Machine.
