"""main.py"""
import logging

def main() -> None:
    """
    Main function to manage server reboots for offline servers.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info("Create a script to rotate logs every 24 hours")

if __name__ == "__main__":
    main()
