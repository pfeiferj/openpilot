# VTSC - Vision Turn Speed Control
Uses the predicted driving path from the model to limit speed when entering
and during curves.

# Status
Experimental

This is my initial implementation of a refactor of the move-fast vision turn
controller. My first test drives show promise for the experience compared to
the existing implementation. Still needs tuning of the acceleration targets as
well as some cleanup and visual indicators of its status in the ui.

# Why two patch files?
Currently the plan is for the changes in the first patch file to be merged
upstream into openpilot. Once merged thatwould make the second patch the only
code needed for the VTSC implementation. If the upstream PR gets rejected I
will merge the two patch files into a single patch instead.
