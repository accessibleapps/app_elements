# Goal

Give users a clear translated issue-submission failure and next action.

# State

Isolated branch based on improve/integration-contract (PR #1). Changes only the
failure wording and logger message in the existing asynchronous reporting action.
Tests exercise failure, success metadata and cancellation through the generator.

# Decisions and why

Keep report collection/send machinery and existing dialog lifetime. Say the report
was not submitted and offer retry later rather than guessing a network/auth cause.
Use the existing app_elements translation registration; no fabricated translations
or binary catalog edits. New source messages fall back to English until translated.

# Surprises

The original failure text did not explain an action. This slice changes no protocol,
transport, async scheduling, cancellation policy or issue_reporter implementation.

# Next step

Publish and read CI. Controlled generator/service tests do not establish real wx
scheduling, server delivery or live screen-reader output. No merge or release.
