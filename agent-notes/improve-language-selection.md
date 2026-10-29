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

PR #2's initial CI passed, but the Chinese fixture used Locale.parse, unlike the
real i18n_core.locale_from_locale_id producer (Locale(language, territory)). The
direct Chinese constructor fails with UnknownLocaleError under Babel 2.17.0, so
those locales are skipped by that producer; claiming they reached the panel was
wrong. Removed unnecessary requested-locale parsing and corrected the existing
regression to use supported real catalog identities: this package's fr/fr_CA and
QRead's hi_IN. Every fixture now uses the producer's direct-constructor shape.
Persisting str(locale) preserves the supplied identity. Chinese discovery is an
upstream i18n_core limitation, not fixed or claimed fixed in this PR.

# Next step

Publish the focused PR and read hosted CI. Tests use real Babel and controlled
fields/services; no live wx or screen-reader result is claimed. No merge/release.
