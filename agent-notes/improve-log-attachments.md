# Goal

Attach the previous session's error log to issue reports when it exists.

# State

Collect the existing current error log and its .old sibling through the existing log_paths list. Omit missing files, directories and an unavailable error_log_path. Preserve dialog cancellation, metadata, send scheduling and reporting text. Independently based on integrated master; integration PR #1 has now been merged by other work, so its existing composition CI is on master. No open PR is this branch's base. Rebased after #2-#6 merged: #5 removed `import os` from interface.py, so the file check uses pathlib like #5's code. #6's success test expected a nonexistent log to be attached; it now supplies real errors.log/errors.log.old files, and a second test covers missing logs.

# Decisions and why

app_framework renames errors.log to errors.log.old on the next startup. A report submitted after restarting otherwise omits the preceding crash evidence. issue_reporter already accepts multiple paths; no transport or storage changes are needed. The missing-path behavior also works with app_framework's separate failed-logging PR.

# Surprises

The report-feedback worktree has separate changes in progress. This branch does not modify it or include its reporting-wording change.

# Next step

Read this PR's existing composition CI. File presence checks do not guarantee a file remains available until the sender opens it. No production submission, merge or release.
