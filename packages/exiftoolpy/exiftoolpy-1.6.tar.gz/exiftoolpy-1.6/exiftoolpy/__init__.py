import subprocess
from pathlib import Path


def exiftool(*args):
    command = './exiftool'
    current_dir = Path(__file__).parent
    try:
        result = subprocess.run([command] + list(args), cwd=current_dir, text=True, capture_output=True)
    except UnicodeDecodeError as e:
        result = subprocess.run([command] + list(args), cwd=current_dir, text=False, capture_output=True)
    if isinstance(result.stderr, bytes):
        stdout = result.stdout.decode('utf-8', errors='ignore')
        stderr = result.stderr.decode('utf-8', errors='ignore')
    else:
        stdout = result.stdout
        stderr = result.stderr
    return stdout, stderr

# subprocess.run(["which", "exiftool"], text=True, capture_output=True)

print(exiftool('-ver'))