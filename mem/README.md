# mem
A utility class for sharing memory across processes. Uses files in /dev/shm (shared memory) to store data and uses a simple locking mechanism to prevent processes from reading mid write. Prevents changes to cereal from being necessary.

This doesn't add any features to openpilot itself and is intended to be used when building other patches.

"A significantly worse cereal." - me


## Branch
[pfeifer-mem](https://github.com/pfeiferj/openpilot/tree/pfeifer-mem)

## Status
Experimental

Known working but locking mechanism could have additional safety.

## Comment Blocks Text
PFEIFER - mem

## API Usage
Coming soon...
