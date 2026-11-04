# Igor showcase — preparation only

TODO-CLAUDE: separate sanitized showcase, not a mirror of the live Igor repository. Planned link: https://github.com/JonathanDolan1/igor-showcase . This batch creates no repository, source copy, public push or deployment.

## Proposed modules (read from the existing source)

| Candidate | Why it helps explain the project | Sanitization before a separate publication |
| --- | --- | --- |
| `~/dev/orchestrator/orch/quiet.py`, especially `in_quiet_hours` at line 30 | Small, stdlib-only example of validated time windows, midnight crossing and explicit boundaries. | Use synthetic hours and examples; publish its focused offline tests only after review. |
| `~/dev/orchestrator/orch/speech_in.py`, only `decode_command` at line 107 and `decode_audio` at line 116 | Shows a defensive audio-processing boundary: fixed format, timeout, missing-tool errors and malformed-output checks. | Extract only the pure decoder boundary; replace all paths and test audio with synthetic fixtures. Omit downloads, provider handling and runtime setup. |
| `~/dev/orchestrator/orch/selfstatus.py`, only `classify_starts` at line 102 | Shows how clean restarts and unclean stops are classified from a small event stream. | Extract the classifier and generic event markers; use synthetic logs, omit journal collection, identifiers and historic incident details. |

AI coding agents wrote most of Igor under Jonathan's direction and review. These modules are candidates, not proof that he wrote each function personally. Before publication he should be able to explain each input, branch, failure and test. Do not copy the repository wholesale. README and architecture diagram are separate TODO-CLAUDE deliverables.

## Stack verification — 4 Nov 2026

“Today” below means 4 Nov in Israel. Source was inspected without environment files, credentials, configured endpoint URLs, personal identifiers or raw log output. The existing running service was inspected read-only; no restart, deploy, remote configuration change, paid API call or message occurred.

| Requested integration | Present in current code/deploy? | In use today? | Evidence and decision |
| --- | --- | --- | --- |
| iCloud CalDAV | **No implementation found.** The one CalDAV reference is a future-migration comment. | **No evidence; do not claim active use.** | `~/dev/orchestrator/orch/config.py:420` says calendar writes need the Mac until migration to CalDAV. `~/dev/orchestrator/mac-agent/handlers/applecalendar.py` and `calendaredit.py` are the current Mac calendar routes; `RUNBOOK.md:233` also describes CalDAV as future work. No CalDAV client import was found in inspected current implementation paths. iCloud/Apple calendar functionality does not establish CalDAV use. Keep TODO-VERIFY or remove CalDAV in final copy. |
| healthchecks.io | **Yes.** | **Yes, active heartbeat confirmed.** | `orch/scheduler.py:580–621` sends the heartbeat and writes a successful-check timestamp; `deploy/rotate-healthcheck.sh` contains the provider's domain without any configured value being returned. Live read-only `data/orch.db`, `kv` entry `heartbeat_last_ok`, was `2026-11-04T14:06:49Z` (16:06:49 Israel time). Service active at verification. No provider page, configured URL or environment file was opened. The timestamp proves a successful heartbeat; provider dashboard/delivery was not independently inspected. |
| Whisper local speech-to-text | **Yes.** | **No same-day transcription verified.** The current running service's last startup reported speech ready; actual use today remains unknown. | `orch/speech_in.py:47–97` implements the local faster-whisper engine; `orch/main.py:122–141` checks readiness at startup. Live source matches these paths. Current service has run since 1 Nov 17:25:36 Israel time; readiness log markers exist on 1 Nov with no not-ready/disabled markers in the inspected window. Today's journal has zero speech markers. Keep TODO-VERIFY for an “in use today” claim; do not equate availability with an actual transcription. |

The yes/no findings intentionally distinguish missing implementation, confirmed heartbeat activity, and unverified same-day speech activity. Missing speech evidence does not mean the feature is broken or unused historically.

## Next step

TODO-CLAUDE: final public wording and architecture diagram. If current-use proof for speech is still needed, agree on a separately authorized safe verification with Jonathan; do not send a message, read personal content, inspect environment files or trigger a paid service from this batch. The portfolio currently labels that claim unverified.
