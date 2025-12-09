# bin2fds.py
FDS and BIN are two different file formats for storing disk images usable with a certain game console. These images can be used with various tools including console emulators and also verious storage device emulators usable with the physical console.
This is a Python 2 script that can sometimes convert .BIN to .FDS in cases where the .FDS itself wasn't being created reliably.

## Usage
it's super ugly but you run it like this:
```bash
python2 bin2fds.py input.bin output.fds
```
or (for multiple-side games)
```bash
python2 bin2fds.py input1.bin input2.bin etc... output.fds
```
