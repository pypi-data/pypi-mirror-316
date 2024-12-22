import subprocess
import sys
from playsound import playsound

def run_command_with_notification():
    if len(sys.argv) < 2:
        print("Usage: notify <command> [args...]")
        sys.exit(1)

    # The command to run
    command = sys.argv[1:]
    sound_file = "alert.wav"  # Default notification sound

    try:
        # Run the terminal command
        process = subprocess.run(command, check=True, shell=True)
        print("Command completed successfully.")
        
        # Play the notification sound
        playsound(sound_file)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}.")
        playsound(sound_file)  # Optionally, we can use a different sound for failures.
    except Exception as e:
        print(f"An error occurred: {e}")

