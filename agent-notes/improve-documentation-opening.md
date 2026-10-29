# Goal

Open an existing localized documentation file through a valid file URI.

# State

Isolated branch based on improve/integration-contract (PR #1). Existing action
name and bundled/source layouts are preserved. Tests cover exact, base-language
and root fallback, missing documentation and URI escaping.

# Decisions and why

Check readme.html itself rather than the locale directory. Use pathlib as_uri
for Windows separators, Unicode and reserved URL characters. An incomplete
locale folder no longer blocks a valid language/root document. Show a translated
warning when no document exists. No manifest field or remote fallback added.

# Surprises

The existing function opened nonexistent files whenever a localized directory
existed without readme.html. No actual packaged app was launched during this work.

# Next step

Publish and read PR CI; controlled browser calls and real temporary filesystem
fixtures do not establish packaged-product or live screen-reader behavior.
