import os

path = os.path.join("..", "assets", "map.umd")

if os.path.exists(path):
    os.remove(path)

print("Map deleted")