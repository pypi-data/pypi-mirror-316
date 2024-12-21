# ANSI escape codes for Linux terminal colors
RESET = "\033[0m"

# Standard colors (foreground)
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# Bright colors (foreground)
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# Bright background colors
BG_BRIGHT_BLACK = "\033[100m"
BG_BRIGHT_RED = "\033[101m"
BG_BRIGHT_GREEN = "\033[102m"
BG_BRIGHT_YELLOW = "\033[103m"
BG_BRIGHT_BLUE = "\033[104m"
BG_BRIGHT_MAGENTA = "\033[105m"
BG_BRIGHT_CYAN = "\033[106m"
BG_BRIGHT_WHITE = "\033[107m"

# Print all colors for testing
def display_colors():
    print(f"{BLACK}BLACK{RESET}")
    print(f"{RED}RED{RESET}")
    print(f"{GREEN}GREEN{RESET}")
    print(f"{YELLOW}YELLOW{RESET}")
    print(f"{BLUE}BLUE{RESET}")
    print(f"{MAGENTA}MAGENTA{RESET}")
    print(f"{CYAN}CYAN{RESET}")
    print(f"{WHITE}WHITE{RESET}")
    
    print(f"{BRIGHT_BLACK}BRIGHT_BLACK{RESET}")
    print(f"{BRIGHT_RED}BRIGHT_RED{RESET}")
    print(f"{BRIGHT_GREEN}BRIGHT_GREEN{RESET}")
    print(f"{BRIGHT_YELLOW}BRIGHT_YELLOW{RESET}")
    print(f"{BRIGHT_BLUE}BRIGHT_BLUE{RESET}")
    print(f"{BRIGHT_MAGENTA}BRIGHT_MAGENTA{RESET}")
    print(f"{BRIGHT_CYAN}BRIGHT_CYAN{RESET}")
    print(f"{BRIGHT_WHITE}BRIGHT_WHITE{RESET}")
    
    print(f"{BG_BLACK}BG_BLACK{RESET}")
    print(f"{BG_RED}BG_RED{RESET}")
    print(f"{BG_GREEN}BG_GREEN{RESET}")
    print(f"{BG_YELLOW}BG_YELLOW{RESET}")
    print(f"{BG_BLUE}BG_BLUE{RESET}")
    print(f"{BG_MAGENTA}BG_MAGENTA{RESET}")
    print(f"{BG_CYAN}BG_CYAN{RESET}")
    print(f"{BG_WHITE}BG_WHITE{RESET}")
    
    print(f"{BG_BRIGHT_BLACK}BG_BRIGHT_BLACK{RESET}")
    print(f"{BG_BRIGHT_RED}BG_BRIGHT_RED{RESET}")
    print(f"{BG_BRIGHT_GREEN}BG_BRIGHT_GREEN{RESET}")
    print(f"{BG_BRIGHT_YELLOW}BG_BRIGHT_YELLOW{RESET}")
    print(f"{BG_BRIGHT_BLUE}BG_BRIGHT_BLUE{RESET}")
    print(f"{BG_BRIGHT_MAGENTA}BG_BRIGHT_MAGENTA{RESET}")
    print(f"{BG_BRIGHT_CYAN}BG_BRIGHT_CYAN{RESET}")
    print(f"{BG_BRIGHT_WHITE}BG_BRIGHT_WHITE{RESET}")

# Run the function to display all colors
if __name__ == "__main__":
    display_colors()
