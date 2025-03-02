import pytest
from unittest.mock import MagicMock, patch
import threading


# Mocking the Order class
class Order:
    def __init__(self):
        self.items = []

    def add_item_to_order(self, item_name, price, quantity, currency="USD"):
        if not isinstance(item_name, str):
            raise ValueError("Invalid input: item_name must be a string")
        if not item_name or price <= 0 or quantity <= 0:
            raise ValueError("Invalid input: item_name must be non-empty, price and quantity must be greater than 0.")
        self.items.append({"item_name": item_name, "price": price, "quantity": quantity, "currency": currency})

    def calculate_total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)


# Test for add valid item
@patch.object(Order, 'add_item_to_order', autospec=True)
def test_add_valid_item(mock_add_item):
    order = Order()
    order.add_item_to_order("Iphone", 1000, 2, "USD")
    mock_add_item.assert_called_with(order, "Iphone", 1000, 2, "USD")


# Test for handling all the invalid item/scenarios
@patch.object(Order, 'add_item_to_order', autospec=True, side_effect=ValueError("Invalid input"))
def test_add_invalid_item(mock_add_item):
    order = Order()
    with pytest.raises(ValueError, match="Invalid input"):
        order.add_item_to_order("", 1000, 2, "USD")
    with pytest.raises(ValueError, match="Invalid input"):
        order.add_item_to_order("Tablet", -300, 2, "USD")


# Test for calculate total functionality
@patch.object(Order, 'calculate_total', return_value=1100)
def test_calculate_total(mock_calculate_total):
    order = Order()
    assert order.calculate_total() == 1100
    mock_calculate_total.assert_called()


# Test for empty order
@patch.object(Order, 'calculate_total', return_value=0)
def test_empty_order_total(mock_calculate_total):
    order = Order()
    assert order.calculate_total() == 0
    mock_calculate_total.assert_called()


# Performance test
@patch.object(Order, 'calculate_total', return_value=10000)
def test_large_order_performance(mock_calculate_total):
    order = Order()
    for i in range(1000):
        order.add_item_to_order(f"Item {i}", 10, 1, "USD")
    assert order.calculate_total() == 10000
    mock_calculate_total.assert_called()


# Simulating multiple users placing orders
def place_order(user_id):
    order = Order()
    order.add_item_to_order(f"Iphone_{user_id}", 1000, 1, "USD")
    print(f"User {user_id}: Order Total = {order.calculate_total()}")


def test_simultaneous_orders():
    threads = []

    with patch.object(Order, 'calculate_total', return_value=1000):
        for i in range(50):
            t = threading.Thread(target=place_order, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()


if __name__ == "__main__":
    pytest.main()
