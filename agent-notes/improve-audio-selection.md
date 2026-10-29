# Goal

Correct the existing audio settings panel without changing product call sites.

# State

Isolated branch based on improve/integration-contract (PR #1). Output and input
population share one small private method. Tests cover configuration defaults,
unavailable equipment, selection fallback, saving and preservation.

# Decisions and why

Use the framework's existing configuration accessor. Disabled empty controls
cannot save a nonexistent choice. Failed input initialization (sound_input=None)
does not prevent output settings from working. Register this module's existing
labels in the app_elements translation domain. Device initialization and applying
settings remain owned by app_framework and products.

# Surprises

sound_lib output enumeration can return no items; input initialization can fail
while the manifest recording flag remains true. Both occur in real source paths.

# Next step

Publish the focused PR and read its CI result. Tests double native/service
boundaries; no live audio, native wx or screen-reader result claimed. No merge.
