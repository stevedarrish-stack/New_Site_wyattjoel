# Backup Index

This file tracks recoverable backup points for the WyattJoel site.

## Final Recovery Backup (2026-02-20)

- Backup name: `final-backup-20260220-122954`
- Commit snapshot: `0383b5c`
- Git backup branch: `codex/final-backup-20260220-122954`
- Git backup tag: `final-backup-20260220-122954`
- Zip backup file: `site-backup-final-20260220-122954.zip`
- Zip SHA-256: `fb73925f3eb740ce7d98f0f67cca13757a6904d06a98639ad50a4bd41a633b4a`
- Zip size: `15M`

## How To Recover

1. Restore from tag:
   `git checkout final-backup-20260220-122954`
2. Or restore from branch:
   `git checkout codex/final-backup-20260220-122954`
3. Redeploy by pushing to publish branch:
   `git push origin HEAD:publish-wyattjoel`
