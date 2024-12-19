import subprocess
import traceback
import os
def main():
    print("hello world")


def spawn():
    path =  os.path.join(os.path.dirname(__file__), "app")
    try:
        result = subprocess.run([path], stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        print(result.stdout)
    except Exception:
        traceback.print_exc()
        print(Exception)
