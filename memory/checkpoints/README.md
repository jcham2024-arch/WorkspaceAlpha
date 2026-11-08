# Checkpoints

One file per session-task: <YYYY-MM-DD>-<slug>.md. Written at
stage 04 (verify) and read at stage 01 (navigate) of the next
session. A checkpoint is the resume point if a session dies:
what was decided, what is still open, which files prove it.

Format:

    # <date> — <task slug>
    ## Decisions
    - ...
    ## Open
    - ...
    ## Proof
    - <file>:<line> or wiki anchor

Keep each checkpoint under ~30 lines; token cost is the point.
