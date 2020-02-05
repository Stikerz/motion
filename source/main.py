import argparse
import os
import sys

from motion.source.cash_machine import CashMachine


def load(instance: CashMachine, amount, coin) -> None:
    instance.load_cash_machine(amount, coin)


def exchange(instance: CashMachine, cash) -> None:
    instance.exchange_cash(cash)


def main(args):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("path", help="path of file")
    args = parser.parse_args(args)

    file = args.path
    if not os.path.isfile(file):
        print("The path specified does not exist or is not a file")
        sys.exit()

    machine = CashMachine()
    with open(file, "r") as reader:
        for line in reader.readlines():
            entry = line.split()

            if entry[0] == "LOAD":
                print(f"{entry[0]} {entry[1]} {entry[2]}")
                load(machine, entry[1], entry[2])
            elif entry[0] == "EXCHANGE":
                print(f"{entry[0]} {entry[1]}")
                exchange(machine, entry[1])
            else:
                print(f"Invalid Command {entry[0]}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
