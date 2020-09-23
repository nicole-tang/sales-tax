import argparse
import sys
import re
import math

BASIC_TAX_RATE = 0.1
IMPORTED_TAX_RATE = 0.05
EXEMPTION = {"book", "food", "chocolate", "medical", "pills"}
IMPORTED = "imported"
ROUND_TO_NEAREST = 0.05


class Util:
    @staticmethod
    def rounding(val):
        """
        np/100 rounded up to the nearest 0.05
        :param val: value to be rounded up
        :return: value rounded up
        """
        if val < 0:
            raise ValueError("Value to be rounded must be larger than 0")
        return math.ceil(val / ROUND_TO_NEAREST) * ROUND_TO_NEAREST

    @staticmethod
    def parse_line(line):
        """
        parse the line item "1 chocolate bar at 3.00" into name: chocolate bar, qty: 1 and unit_price 3.00
        :param line: an item from the receipt
        :return: dictionary of key name, qty, unit_price
        """
        try:
            name = re.findall(r"\d (.*?) at", line)[0]
            qty, unit_price = re.findall(r"\d*\.\d+|\d+", line)
        except (IndexError, ValueError):
            raise ValueError(
                "Invalid line format: the line must be in format of: <qty> <name> at <price>"
            )
        qty = int(qty)
        unit_price = float(unit_price)
        return {"name": name, "qty": qty, "unit_price": unit_price}


class Item:
    def __init__(self, name, qty, unit_price):
        """
        :param name: name of the item
        :param qty: quantity of the item
        :param unit_price: unit price of the item
        """
        self.qty = qty
        self.unit_price = unit_price
        self.name = name
        self.tax = self.calculate_tax()
        self.subtotal = (self.unit_price * self.qty) + self.tax

    def calculate_tax(self):
        """
        calculate the tax required for the item
        :return: a rounded up tax amount
        """
        tax_rate = BASIC_TAX_RATE

        if self.is_exempted():
            tax_rate = 0

        if IMPORTED in self.name:
            tax_rate += IMPORTED_TAX_RATE

        return Util.rounding(self.unit_price * self.qty * tax_rate)

    def is_exempted(self):
        """
        Currently only keywords in the EXEMPTION list would be consider as exempted.
        Ideally, a more scalable approach would be to gather the information of which
        category does the item belong and check whether the category is in exemption list.
        This can be done so by:
        1. external API
        2. extensive list of data
        3. machine learning model (?)
        """
        return any([e in self.name for e in EXEMPTION])


class Receipt:
    def __init__(self, lines):
        """
        :param lines: input from the text file
        """
        self.lines = lines
        self.tax = 0
        self.total = 0

    def print_receipt(self):
        """
        print on console the desire format of the receipt for each item
        """
        for l in self.lines:
            item = Item(**Util.parse_line(l))
            self.total += item.subtotal
            self.tax += item.tax
            print("{} {}: {:.2f}".format(item.qty, item.name, item.subtotal))

        print("Sales Taxes: {:.2f}".format(self.tax))
        print("Total: {:.2f}".format(self.total))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="file path of the input file",
    )
    file = parser.parse_args().file

    # parse the text file
    items = [line.strip() for line in file.readlines() if line.strip()]

    Receipt(items).print_receipt()
