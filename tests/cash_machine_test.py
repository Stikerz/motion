import unittest
import contextlib
from io import StringIO
import pathlib
import os

from source.cash_machine import CashMachine
from source.main import main
from unittest import mock


class CashMachineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = CashMachine()

    def test_cashmachine_load_machine_20_p(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.load_cash_machine("50", "0.20")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(
            output[0], "0 2£, 0 1£, 0 0.50£, 50 0.20£, 0 5£, 0 10£,  0 20£"
        )
        self.assertEqual(self.machine.coins["0.20"], 50)

    def test_cashmachine_load_machine_50_p(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.load_cash_machine("50", "0.50")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(
            output[0], "0 2£, 0 1£, 50 0.50£, 0 0.20£, 0 5£, " "0 10£,  0 20£"
        )
        self.assertEqual(self.machine.coins["0.50"], 50)

    def test_cashmachine_load_machine_2_pound(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.load_cash_machine("50", "2")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(
            output[0], "50 2£, 0 1£, 0 0.50£, 0 0.20£, 0 5£, " "0 10£,  0 20£"
        )
        self.assertEqual(self.machine.coins["2"], 50)

    def test_cashmachine_load_machine_1_pound(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.load_cash_machine("50", "1")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(
            output[0], "0 2£, 50 1£, 0 0.50£, 0 0.20£, 0 5£, " "0 10£,  0 20£"
        )
        self.assertEqual(self.machine.coins["1"], 50)

    def test_cashmachine_load_incorrect_command(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.load_cash_machine("50", "50")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "Unable to load 50")

    def test_cashmachine_exhange_machine_5_error(self):
        self.machine.load_cash_machine("50", "2")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("5")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "CANNOT EXCHANGE")
        self.assertEqual(
            output[1], "50 2£, 0 1£, 0 0.50£, 0 0.20£, 0 5£, " "0 10£,  0 20£"
        )

    def test_cashmachine_exhange_machine_5(self):
        self.machine.load_cash_machine("50", "2")
        self.machine.load_cash_machine("50", "1")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("5")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "2 2£, 1 1£, 0 0.50£, 0 0.20£")
        self.assertEqual(
            output[1], "48 2£, 49 1£, 0 0.50£, 0 0.20£, 1 5£, " "0 10£,  0 20£"
        )

    def test_cashmachine_exhange_machine_10_error(self):
        self.machine.load_cash_machine("1", "2")
        self.machine.load_cash_machine("7", "1")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("10")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "CANNOT EXCHANGE")
        self.assertEqual(
            output[1], "1 2£, 7 1£, 0 0.50£, 0 0.20£, 0 5£, " "0 10£,  0 20£"
        )

    def test_cashmachine_exhange_machine_10(self):
        self.machine.load_cash_machine("20", "2")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("10")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "5 2£, 0 1£, 0 0.50£, 0 0.20£")
        self.assertEqual(
            output[1], "15 2£, 0 1£, 0 0.50£, 0 0.20£, 0 5£, " "1 10£,  0 20£"
        )

    def test_cashmachine_exhange_machine_20_error(self):
        self.machine.load_cash_machine("99", "0.20")
        self.machine.load_cash_machine("1", "0.50")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("20")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "CANNOT EXCHANGE")
        self.assertEqual(
            output[1], "0 2£, 0 1£, 1 0.50£, 99 0.20£, 0 5£, " "0 10£,  0 20£"
        )

    def test_cashmachine_exhange_machine_20(self):
        self.machine.load_cash_machine("150", "0.20")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("20")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "0 2£, 0 1£, 0 0.50£, 100 0.20£")
        self.assertEqual(
            output[1], "0 2£, 0 1£, 0 0.50£, 50 0.20£, 0 5£, " "0 10£,  1 20£"
        )

    def test_cashmachine_exhange_incorrect_command(self):
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            self.machine.exchange_cash("50")
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "Unable to exchange 50")



class MainTest(unittest.TestCase):
    def test_incorrect_path(self):
        with self.assertRaises(SystemExit):
            working_dir = pathlib.Path().absolute()
            test_file = os.path.join(working_dir, "fake_gfg.txt")

            temp_stdout = StringIO()
            with contextlib.redirect_stdout(temp_stdout):
                main([test_file])
            output = temp_stdout.getvalue().splitlines()
            self.assertEqual(
                output[0], "The path specified does not exist or " "is not a file"
            )

    @mock.patch("source.main.exchange")
    @mock.patch("source.main.load")
    def test_correct_calls(self, load, exchange):
        working_dir = pathlib.Path().absolute()
        test_file = os.path.join(working_dir, "input.txt")
        main([test_file])
        self.assertTrue(exchange.called)
        self.assertEqual(4, exchange.call_count)
        self.assertTrue(load.called)
        self.assertEqual(2, load.call_count)

    def test_invalid_command(self):
        working_dir = pathlib.Path().absolute()
        test_file = os.path.join(working_dir, "invalid.txt")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            main([test_file])
        output = temp_stdout.getvalue().splitlines()
        self.assertEqual(output[0], "Invalid Command INVALID")
