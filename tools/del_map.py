import os

path = os.path.join("..", "saves", "map.umd")

if os.path.exists(path):
    os.remove(path)

print("Map deleted")