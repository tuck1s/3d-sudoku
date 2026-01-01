#!/usr/bin/env bash
set -e

# cube 8  → nice 10
# sudo renice -n 10 -p 20293

# cube 9  → nice 9
sudo renice -n 9  -p 20294

# cube 10 → nice 9
sudo renice -n 9  -p 20295

# cube 11 → nice 8
sudo renice -n 8  -p 20296

# cube 12 → nice 4
sudo renice -n 4  -p 20297

# cube 13 → nice 4
sudo renice -n 4  -p 20298

# cube 14 → nice 3
sudo renice -n 3  -p 20299

# cube 15 → nice 0
sudo renice -n 0  -p 20300

# cube 16 → nice 7
sudo renice -n 7  -p 20301

# cube 17 → nice 3
sudo renice -n 3  -p 20302

# cube 18 → nice 2
sudo renice -n 2  -p 20303

echo "Done."
