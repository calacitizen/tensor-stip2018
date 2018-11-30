import os
from sys import platform as _platform

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


if _platform == "linux" or _platform == "linux2":
    # linux
    pass
elif _platform == "darwin":
    # MAC OS X
    STOCKFISH_PATH = "stockfish/Mac/"
elif _platform == "win32":
    # Windows
    pass
elif _platform == "win64":
    # Windows 64-bit
    pass