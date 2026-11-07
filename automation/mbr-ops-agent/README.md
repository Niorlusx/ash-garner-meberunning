# MBR Ops Agent

Managed Mistral Workflow worker for MBR Records (Ash Garner / 3630).

**Workflow:** `mbr-daily-ops` - daily deterministic ops pipeline:
- SoundCloud upload queue (6 tracks pending)
- YouTube / YTM queue (5 items)
- Store delivery request list (13 tracks via SoundCloud for Artists)
- Control Room daily checks
- Private Lane guard (Shakeah tracks + Earn Back Trust stay private)

Deployed as a managed deployment; the platform injects the service-account
token, no API keys in the repo. Scheduled daily via Mistral workflow schedules.

Voice rule: Ashley Garner on the article, Ash Garner on the song.
© 2026 MBR Records. Shepparton, Victoria (3630).
