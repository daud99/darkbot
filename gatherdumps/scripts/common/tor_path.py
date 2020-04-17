from pathlib import Path
import os
def get_path():
    home_path = str(Path.home())
    x = '/home/darkbot'+"/Files/tor-browser_en-US"
    return x 

if __name__ == "__main__":
    get_path()
'''
x = str(Path.home())
print(x)
y = os.path.abspath("Files")
print(y)
'''
