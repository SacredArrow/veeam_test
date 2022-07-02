# File synchronizer

This program periodically checks base directory for changes and changes target directory accordingly.

### Usage
`python3 main.py base_dir target_dir log_file synchronization_period`

`base_dir` - Directory which will be monitored

`target_dir` - Directory which will be changed

`log_file` - File where all manipulations will be logged

`synchronization_period` - Time between synchronization rounds (in seconds, might be floating-point)

#### Example

`python3 main.py D:\Folder ./folderCopy ./log.txt 3`