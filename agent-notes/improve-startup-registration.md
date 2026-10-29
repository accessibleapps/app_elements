# Goal

Correct the existing Windows startup panel and registration command.

# State

PR #4 is open. Initial CI ran 11 tests; ten passed and the save-failure regression
errored because its get_executable double returned Mock instead of a path string.
Corrected that fixture so it reaches the intended CreateKeyEx permission error.
No production relaxation or added guard; waiting for repaired-head CI.

Isolated branch based on improve/integration-contract (PR #1). Public panel and
get_startup/set_startup names are unchanged. No system registry writes performed
by development/tests; tests use a controlled winreg boundary.

# Decisions and why

Set the rendered checkbox's live value. Missing key/value means disabled; other
read failures propagate. Enable with CreateKeyEx/KEY_SET_VALUE and REG_SZ; disable
only this application's value with KEY_SET_VALUE. A missing disable is idempotent.
Use stdlib subprocess.list2cmdline for the Windows command; source launches include
sys.executable because platform_utils returns the main script when not frozen.
No existing platform_utils command builder was found. Low-level write errors
propagate; the panel logs and displays a translated warning on save failure.
The startup and audio labels now explicitly bind their app_elements domain.

# Surprises

The package still supports Python 3 only, so the Python 2 _winreg import fallback
is removed. Startup remains explicitly Windows-only. No startup launch measured.

# Next step

Publish focused PR and read CI. No live Windows startup/AT claim, merge or release.
