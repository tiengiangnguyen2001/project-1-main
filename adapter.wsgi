import os
import sys

path = os.path.dirname(__file__)
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from app import application