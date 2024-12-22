import subprocess


def exiftool(*args):
    command = 'exiftool-13.10/exiftool'
    try:
        result = subprocess.run([command] + list(args), text=True, capture_output=True)
    except UnicodeDecodeError as e:
        result = subprocess.run([command] + list(args), text=False, capture_output=True)
    if isinstance(result.stderr, bytes):
        stdout = result.stdout.decode('utf-8', errors='ignore')
        stderr = result.stderr.decode('utf-8', errors='ignore')
    else:
        stdout = result.stdout
        stderr = result.stderr
    return stdout, stderr