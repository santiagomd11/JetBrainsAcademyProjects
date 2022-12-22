import logging
import sys
import shutil
import argparse


class FlashCard:
    def __init__(self):
        self.definitions_term_dict = {}
        self.__fails_attempts = {}
        self.__temp_file = 'logs.txt'
        self.__end = False

    def init_logs(self):
        # logs configuration
        handlers = [logging.FileHandler(self.__temp_file), logging.StreamHandler(sys.stdout)]
        logging.basicConfig(handlers=handlers, level=logging.DEBUG, format="%(message)s")

    def add(self):
        end_card = False
        while not end_card:
            logging.debug("The card:")
            card = input()
            if card in self.definitions_term_dict.keys():
                logging.debug(f'The card "{card}" already exists. Try again:')
            else:
                self.definitions_term_dict.setdefault(card, "")
                end_card = True

        end_definition = False
        while not end_definition:
            logging.debug("The definition of the card:")
            definition = input()
            if definition in self.definitions_term_dict.values():
                logging.debug(f'The definition "{definition}" already exists. Try again:')
            else:
                self.definitions_term_dict[card] = definition
                end_definition = True
        logging.debug(f'The pair ("{card}":"{definition}") has been added.')

    def remove(self):
        logging.debug("Which card?")
        card = input()
        if card in self.definitions_term_dict.keys():
            del self.definitions_term_dict[card]
            logging.debug("The card has been removed.")
        else:
            logging.debug(f'Can\'t remove "{card}": there is no such card.')

    def import_from_file(self, file_name):
        try:
            with open(file_name, "r") as f:
                for line in f.readlines():
                    card, definition = line.split(":")
                    self.definitions_term_dict[card.strip()] = definition.strip()
            logging.debug(f'{len(self.definitions_term_dict.keys())} cards have been loaded.')
        except FileNotFoundError:
            logging.debug("File not found.")
            pass

    def export(self, file_name):
        with open(file_name, "w") as f:
            for key, value in self.definitions_term_dict.items():
                f.write(f'{key}: {value}\n')
        logging.debug(f"{len(self.definitions_term_dict.keys())} cards have been saved.")

    def ask(self, times):
        time = 0
        for _ in range(0, times):
            for key, value in self.definitions_term_dict.items():
                if time == times:
                    break
                else:
                    logging.debug(f'Print the definition of "{key}"')
                    user_input = input()
                    if user_input in self.definitions_term_dict.values():
                        if value == user_input:
                            logging.debug("Correct!")
                        else:
                            user_input_key = list(self.definitions_term_dict.keys())[list(self.definitions_term_dict.values()).index(user_input)]
                            self.__fails_attempts.setdefault(key, 0)
                            self.__fails_attempts[key] += 1
                            logging.debug(f'Wrong. The right answer is "{value}", but your definition is correct for "{user_input_key}".')
                    else:
                        self.__fails_attempts.setdefault(key, 0)
                        self.__fails_attempts[key] += 1
                        logging.debug(f'Wrong. The right answer is "{value}".')
                time += 1

    def log(self):
        logging.debug("File name:")
        filename = input()
        shutil.copy(self.__temp_file, filename)
        logging.debug("The log has been saved.")

    def hardest_card(self):
        if self.__fails_attempts:
            max_value = max(self.__fails_attempts.values())
            if max_value != 0:
                hardest_cards = [f'"{k}", ' for k, v in self.__fails_attempts.items() if v == max_value]
                if len(hardest_cards) == 1:
                    logging.debug(f'The hardest card is {"".join(hardest_cards).strip(", ")}. You have {max_value} errors answering it.')
                else:
                    logging.debug(f'The hardest cards are {"".join(hardest_cards).strip(", ")}. You have {max_value} errors answering them.')
        else:
            logging.debug("There are no cards with errors.")

    def reset_stats(self):
        self.__fails_attempts.clear()
        logging.debug("Card statistics have been reset.")

    def main(self):
        self.init_logs()
        parser = argparse.ArgumentParser()
        parser.add_argument("--import_from")
        parser.add_argument("--export_to")
        args = parser.parse_args()

        if args.import_from:
            self.import_from_file(args.import_from)

        while not self.__end:
            logging.debug("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
            action = input()
            if action == "add":
                self.add()
            elif action == "remove":
                self.remove()
            elif action == "import":
                logging.debug("File name:")
                file_name = input()
                self.import_from_file(file_name)
            elif action == "export":
                logging.debug("File name:")
                file_name = input()
                self.export(file_name)
            elif action == "ask":
                logging.debug("How many times to ask?")
                times = int(input())
                self.ask(times)
            elif action == "log":
                self.log()
            elif action == "hardest card":
                self.hardest_card()
            elif action == "reset stats":
                self.reset_stats()
            elif action == "exit":
                logging.debug("Bye bye!")
                if args.export_to:
                    self.export(args.export_to)
                self.__end = True


if __name__ == "__main__":
    FlashCard().main()
