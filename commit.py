import random
import string
import subprocess
import time
import sys
from datetime import datetime

COMMIT_FILE = "commit.txt"

def count_todays_commits():
    today = datetime.now().strftime("%Y-%m-%d")
    result = subprocess.run(
        ["git", "log", "--oneline", "--after", f"{today} 00:00:00", "--before", f"{today} 23:59:59"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return 0
    return len([l for l in result.stdout.strip().splitlines() if l])

def add_random_character():
    char = random.choice(string.ascii_letters + string.digits)
    with open(COMMIT_FILE, "a") as f:
        f.write(char)
    return char

def build_commit_message(commit_number):
    date_str = datetime.now().strftime("%d-%m-%y")
    return f"add | git contrib {date_str}-{str(commit_number).zfill(2)}"

def animate_spinner(label, duration=1.2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r  \033[96m{frames[i % len(frames)]}\033[0m  {label}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r  \033[92m✔\033[0m  {label}\n")
    sys.stdout.flush()

def animate_progress_bar(label, duration=1.0):
    bar_len = 30
    steps = 30
    for i in range(steps + 1):
        filled = int(bar_len * i / steps)
        bar = "█" * filled + "░" * (bar_len - filled)
        pct = int(100 * i / steps)
        sys.stdout.write(f"\r  \033[93m{label}\033[0m  [{bar}] {pct}%")
        sys.stdout.flush()
        time.sleep(duration / steps)
    sys.stdout.write(f"\r  \033[92m{label}\033[0m  [{'█' * bar_len}] 100%\n")
    sys.stdout.flush()

def git_commit_with_animation(message):
    steps = [
        (["git", "add", "--all"],          "Staging all files...  "),
        (["git", "commit", "-m", message], "Committing changes... "),
        (["git", "push"],                  "Pushing to GitHub...  "),
    ]
    for cmd, label in steps:
        animate_spinner(label, duration=random.uniform(0.8, 1.4))
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"\n  \033[91m✖  Error:\033[0m {result.stderr.strip()}")
            return False
    return True

def print_header():
    print("\n\033[95m" + "━" * 45)
    print("   ██████╗ ██╗████████╗")
    print("  ██╔════╝ ██║╚══██╔══╝")
    print("  ██║  ███╗██║   ██║   ")
    print("  ██║   ██║██║   ██║   ")
    print("  ╚██████╔╝██║   ██║   ")
    print("   ╚═════╝ ╚═╝   ╚═╝   ")
    print("  Auto GitHub Contributor")
    print("━" * 45 + "\033[0m\n")

def print_commit_block(index, total, char, message):
    print(f"  \033[90m{'─' * 40}\033[0m")
    print(f"  \033[97mCommit {index}/{total}\033[0m")
    print(f"  \033[90m Appended '\033[93m{char}\033[90m' → commit.txt\033[0m")
    print(f"  \033[90m Message:  \033[96m{message}\033[0m")

def ask_commit_count():
    """Prompt the user for how many commits to make, with validation."""
    print("  \033[97mHow many commits do you want to make?\033[0m")
    while True:
        try:
            raw = input("  \033[96m→ Enter a number: \033[0m").strip()
            count = int(raw)
            if count <= 0:
                print("  \033[91m✖  Please enter a number greater than 0.\033[0m")
            elif count > 50:
                confirm = input(f"  \033[93m⚠  That's {count} commits — are you sure? (y/n): \033[0m").strip().lower()
                if confirm == "y":
                    return count
            else:
                return count
        except ValueError:
            print("  \033[91m✖  Invalid input. Please enter a whole number.\033[0m")

if __name__ == "__main__":
    print_header()

    base_count = count_todays_commits()
    print(f"  \033[90mCommits already today: \033[97m{base_count}\033[0m\n")

    commits_per_run = ask_commit_count()
    print()

    for i in range(commits_per_run):
        commit_number = base_count + i + 1
        char = add_random_character()
        message = build_commit_message(commit_number)

        print_commit_block(i + 1, commits_per_run, char, message)
        animate_progress_bar("Preparing...          ")

        success = git_commit_with_animation(message)
        if not success:
            print("\n  \033[91mStopping early due to an error.\033[0m")
            break

        print(f"  \033[92m✔  Done!\033[0m\n")
        time.sleep(random.uniform(0.3, 0.7))

    print("\033[95m" + "━" * 45)
    print(f"  ✔︎  {commits_per_run} commits pushed successfully!")
    print("━" * 45 + "\033[0m\n")