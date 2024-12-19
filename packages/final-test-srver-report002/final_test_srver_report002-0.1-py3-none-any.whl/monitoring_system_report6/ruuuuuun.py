import subprocess
import threading
import os

def run_command(command, working_dir):
    try:
        print(f"Running: {command} in {working_dir}")
        subprocess.run(command, cwd=working_dir, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")

def main():
    commands = [
        ("python3 agent.py", "agent"),             # Command and folder for agent
        ("python3 server.py", "server"),          # Command and folder for server
        ("python3 http_bridge.py", "server")      # Command and folder for HTTP bridge
    ]

    threads = []
    for command, working_dir in commands:
        thread = threading.Thread(target=run_command, args=(command, working_dir))
        threads.append(thread)
        thread.start()

    # for thread in threads:
    #     thread.join()

if __name__ == "__main__":
    main()
