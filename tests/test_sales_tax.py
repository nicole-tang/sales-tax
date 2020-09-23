import pytest
from sales_tax import Util, Item, Receipt


class TestUtil:
    @pytest.mark.parametrize(
        "value,expected",
        [(0, 0), (0.02, 0.05), (0.03, 0.05), (0.05, 0.05), (1.57, 1.6)],
    )
    def test_rounding(self, value, expected):
        assert Util.rounding(value) == expected

    def test_rounding_negative(self):
        with pytest.raises(ValueError):
            Util.rounding(-1)

    @pytest.mark.parametrize(
        "line,expected",
        [
            ("1 book at 12.49", {"name": "book", "qty": 1, "unit_price": 12.49}),
            (
                "1 chocolate bar at 0.85",
                {"name": "chocolate bar", "qty": 1, "unit_price": 0.85},
            ),
            (
                "10 box of imported chocolates at 11.25",
                {"name": "box of imported chocolates", "qty": 10, "unit_price": 11.25},
            ),
            (
                "1 random something at 11.00",
                {"name": "random something", "qty": 1, "unit_price": 11.0},
            ),
        ],
    )
    def test_parse_line(self, line, expected):
        assert Util.parse_line(line) == expected

    @pytest.mark.parametrize(
        "line", ["this is an invalid input", "", "1.5 chocolate at 3.0"],
    )
    def test_parse_invalid_line(self, line):
        with pytest.raises(ValueError):
            Util.parse_line(line)


class TestItem:
    @pytest.mark.parametrize(
        "item, tax",
        [
            ({"name": "book", "qty": 1, "unit_price": 12.49}, 0),
            ({"name": "chocolate bar", "qty": 1, "unit_price": 0.85}, 0),
            (
                {"name": "box of imported chocolates", "qty": 10, "unit_price": 11.25},
                5.65,
            ),
            ({"name": "random something", "qty": 1, "unit_price": 11.0}, 1.1),
            (
                {"name": "imported bottle of perfume", "qty": 1, "unit_price": 27.99},
                4.2,
            ),
        ],
    )
    def test_calculate_tax(self, item, tax):
        assert Item(**item).calculate_tax() == tax

    @pytest.mark.parametrize(
        "item, is_exempted",
        [
            ({"name": "book", "qty": 1, "unit_price": 12.49}, True),
            ({"name": "chocolate bar", "qty": 1, "unit_price": 0.85}, True),
            (
                {"name": "box of imported chocolates", "qty": 10, "unit_price": 11.25},
                True,
            ),
            ({"name": "random something", "qty": 1, "unit_price": 11.0}, False),
            (
                {"name": "imported bottle of perfume", "qty": 1, "unit_price": 27.99},
                False,
            ),
            ({"name": "headache pills", "qty": 1, "unit_price": 27.99}, True,),
        ],
    )
    def test_is_exempted(self, item, is_exempted):
        assert Item(**item).is_exempted() == is_exempted


class TestReceipt:
    @pytest.fixture
    def input_items(self):
        with open("test_data/input_3.txt", "r") as r:
            return [line for line in r.readlines() if line.strip()]

    def test_print_receipt(self, input_items, capsys):
        Receipt(input_items).print_receipt()
        out, err = capsys.readouterr()
        assert out == (
            "1 imported bottle of perfume: 32.19\n"
            "1 bottle of perfume: 20.89\n"
            "1 packet of headache pills: 9.75\n"
            "1 box of imported chocolates: 11.85\n"
            "Sales Taxes: 6.70\n"
            "Total: 74.68\n"
        )
