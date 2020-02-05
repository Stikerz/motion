from math import floor
from collections import OrderedDict, defaultdict
from typing import Tuple


class CashMachine:
    def __init__(self):
        self.banknotes = {"5": 0, "10": 0, "20": 0}
        self.coins = OrderedDict({"2": 0, "1": 0, "0.50": 0, "0.20": 0})

    def _dispense_coins(
        self, dispense_amount, pending_coins, machine_c
    ) -> Tuple[defaultdict, OrderedDict]:
        """Recursively goes through coins in machine to reach requested
        amount """
        if dispense_amount == 0:
            return pending_coins, machine_c
        for c, amount in machine_c.items():
            if amount != 0:

                if c == "2" and dispense_amount > 1:
                    pending_coins["2"] += 1
                    machine_c["2"] -= 1
                    dispense_amount -= 2
                    return self._dispense_coins(
                        dispense_amount, pending_coins, machine_c
                    )

                if c == "1":
                    pending_coins["1"] += 1
                    machine_c["1"] -= 1
                    dispense_amount -= 1
                    return self._dispense_coins(
                        dispense_amount, pending_coins, machine_c
                    )

                if c == "0.50" and machine_c["0.50"] > 1:
                    pending_coins["0.50"] += 2
                    machine_c["0.50"] -= 2
                    dispense_amount -= 1
                    return self._dispense_coins(
                        dispense_amount, pending_coins, machine_c
                    )

                if c == "0.20" and machine_c["0.20"] > 4:
                    pending_coins["0.20"] += 5
                    machine_c["0.20"] -= 5
                    dispense_amount -= 1
                    return self._dispense_coins(
                        dispense_amount, pending_coins, machine_c
                    )
        return pending_coins, machine_c

    def _has_enough_money(self, cash, coins) -> bool:
        """Check to see if machine able to exchange cash for coina"""
        two_pound = coins["2"] * 2
        one_pound = coins["1"]
        fifty_p = floor(coins["0.50"] / 2)
        twenty_p = floor(coins["0.20"] / 5)
        return sum([two_pound, one_pound, fifty_p, twenty_p]) == cash

    def _print_machine_balance(self) -> None:
        """Print remaining available balance of cash machine"""
        print(
            f"{self.coins['2']} 2£, {self.coins['1']} 1£, "
            f"{self.coins['0.50']} 0.50£, {self.coins['0.20']} 0.20£, "
            f"{self.banknotes['5']} 5£, {self.banknotes['10']} 10£, "
            f" {self.banknotes['20']} 20£"
        )

    def _print_released_money(self, coins: dict) -> None:
        """Print coin amount released from cash machine"""
        print(
            f"{self.coins['2'] - coins['2']} 2£, "
            f"{self.coins['1'] - coins['1']} 1£, "
            f"{self.coins['0.50'] - coins['0.50']} 0.50£,"
            f" {self.coins['0.20'] - coins['0.20']} 0.20£"
        )

    def exchange_cash(self, cash: str) -> None:
        """Exchange Cash with coins from machine"""
        if cash not in self.banknotes:
            print(f"Unable to exchange {cash}")
        else:
            temp_c = self.coins.copy()
            coins, machine_c = self._dispense_coins(
                int(cash), defaultdict(lambda: 0), temp_c
            )
            if self._has_enough_money(int(cash), coins):
                self._print_released_money(machine_c)
                self.coins = machine_c
                self.banknotes[cash] += 1
            else:
                print("CANNOT EXCHANGE")
            self._print_machine_balance()

    def load_cash_machine(self, amount: str, cash: str) -> None:
        """Load Cash machine with coins"""
        if cash not in self.coins:
            print(f"Unable to load {cash}")
        else:
            self.coins[cash] += int(amount)
            self._print_machine_balance()
