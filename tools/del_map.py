import os
from glob import glob

path = os.path.join("..", "saves", "map.umd")

os.remove(path)

print("Map deleted")