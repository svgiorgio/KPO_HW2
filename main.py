from infrastructure.di import Container
from infrastructure.ui import ConsoleUI

def main():
    container = Container()
    ui = ConsoleUI(container)
    ui.run_demo()

if __name__ == "__main__":
    main()