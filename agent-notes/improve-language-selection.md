# Goal

Fix language selection and persistence for existing product options dialogs.

# State

Isolated branch based on improve/integration-contract (PR #1). Existing public
API is preserved; no consuming app edits or live language switching.

# Decisions and why

Use Babel's complete locale identity for matching/saving and full display names
for regional labels. Prefer exact locale, then base language, another matching
regional locale, then the default. No selection does not save a setting.
The original set_value population call is valid: ChoiceField delegates it to
set_items. The earlier investigation's claim to the contrary was corrected.

# Surprises

Babel resolves zh_CN to zh_Hans_CN, so matching must canonicalize the requested
locale as well as using the locale object's full identity.

# Next step

Publish the focused PR and read hosted CI. Tests use real Babel and controlled
fields/services; no live wx or screen-reader result is claimed. No merge/release.
