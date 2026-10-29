# Goal

Deliver the accepted integration-documentation, tests and CI improvement as its
own PR. Q authorized implementation and separate PRs with "Make it so!".

# State

PR #1 is open. GitHub's repository Actions API reported enabled=false, explaining
the absent checks. Enabled Actions as part of the requested CI work, preserving
its allowed-actions policy. The next substantive push activates PR CI. README
is also wired into distribution metadata. Three baseline tests are present.

Based on origin/master in an isolated worktree; main checkout edits are preserved.
This PR adds a README, controlled unittest harness, two baseline contract tests,
and a Linux CI job for the documented test command and existing Hatchling build.
No runtime dependency, public API or application source changes.

# Decisions and why

Use stdlib unittest and a pinned Babel test dependency without resolving desktop
runtime dependencies. Tests explicitly double wx/services and make no native or
live AT claims. The five repair PRs will target this branch so they use this one
workflow and harness. Each adds its own focused regression file. No merge/release
authorized. Q requested missing tests and CI as part of resolving all findings.

Correction to the initial investigation: ChoiceField.set_value already calls
set_items (gui_builder/fields.py:1083). There is no population bug. The language
repair addresses regional locale identity and labels only.

# Surprises

No tracked CI/test command existed. The README establishes the commands before
the workflow invokes them. No project lock is needed for stdlib tests with the
explicit Babel version; build uses the existing build-system requirements.

# Next step

Publish this PR and read its CI result, then deliver the five focused repair PRs.
