import pytest


def calculate(page, amount, zone):
    page.fill("#amount", amount)
    page.select_option("#zone", zone)
    page.click("#calc")


@pytest.mark.parametrize(
    "amount, zone, expected",
    [
        ("5000", "city", "Доставка: 500 ₸"),
        ("5000", "region", "Доставка: 1000 ₸"),
        ("9999", "city", "Доставка: 500 ₸"),
        ("9999", "region", "Доставка: 1000 ₸"),
        ("10000", "city", "Доставка бесплатно"),    # граница
        ("10000", "region", "Доставка бесплатно"),  # граница
        ("10001", "city", "Доставка бесплатно"),
        ("10001", "region", "Доставка бесплатно"),
        ("0", "city", "Доставка: 500 ₸"),
    ],
)
def test_delivery_cost(page, amount, zone, expected):
    calculate(page, amount, zone)
    assert page.inner_text("#result") == expected


@pytest.mark.parametrize("amount", ["", "abc", "-100"])
def test_invalid_amount_shows_error(page, amount):
    calculate(page, amount, "city")
    assert page.inner_text("#error") == "Введите корректную сумму"
    assert page.inner_text("#result") == ""
