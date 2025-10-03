#A class that adds all the colors needed
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

#All the needed icons
ICONS = {
    "game": "🎮",
    "trophy": "🏆",
    "user": "👤",
    "exit": "❌",
    "star": "⭐",
    "help": "❓",
    "winner": "🥇",
    "loser": "💀",
    "heart": "❤️",
    "check": "✔️",
    "easy": "🌱",
    "medium": "⚔️",
    "hard": "🔥"
}

#
def print_color(text, color):
    print(f"{color}{text}{Colors.ENDC}")