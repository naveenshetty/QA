## Assignment Part - 1

### Question 1: Manual test case provided in Excel sheet refer sheet 

### Automated Test Cases

```python
import pytest
from order import Order
import threading

# Test for add valid item
def test_add_valid_item():
    order = Order()
    order.add_item_to_order("Iphone", 1000, 2)
    assert len(order.items) == 1
    assert order.items[0]["item_name"] == "Iphone"
    assert order.calculate_total() == 2000

# Test for handling all the invalid item/scenarios    
def test_add_invalid_item():
    order = Order()
    with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
        order.add_item_to_order("", 1000, 2)
    with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
        order.add_item_to_order("Tablet", -300, 2)
    with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
        order.add_item_to_order("Tablet", 300, 0)
    with pytest.raises(ValueError, match="Invalid input: item_name must be a string"):
        order.add_item_to_order(123, 1000, 2)

# Test for calculate total functionality        
def test_calculate_total():
    order = Order()
    order.add_item_to_order("Phone", 500, 1)
    order.add_item_to_order("Tablet", 300, 2)
    assert order.calculate_total() == 1100

# Test for empty order    
def test_empty_order_total():
    order = Order()
    assert order.calculate_total() == 0

# Test for checking performance of the application by doing large order    
def test_large_order_performance():
    order = Order()
    for i in range(1000):
        order.add_item_to_order(f"Item {i}", 10, 1)
    assert order.calculate_total() == 10000

# A basic simulation for simultaneous test at a time by 50 user
def place_order(user_id):
    order = Order()
    order.add_item_to_order(f"Iphone_{user_id}", 1000, 1)
    print(f"User {user_id}: Order Total = {order.calculate_total()}")

threads = []
for i in range(50):
    t = threading.Thread(target=place_order, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### Question 2: Early Testing & Collaboration

**These are the approaches during my day-to-day work:**

-  Collaborate with product managers and developers, SME of the product,Business Analyst to clarify requirements.
-  Document test scenarios early, covering positive, negative, and boundary cases.
-  Design test cases before development starts like using **Shift-left testing**
-  I believe following TDD in the project wil also help finding the defect in early and the test cases help ensure that code meets the requirements and works as expected.
-  Discuss testability and review code before execution.
-  Integrate regression tests in pipelines by automated continuous test 
-  Use load and stress testing tools (e.g., JMeter).
-  Encouraging developers to work together with testers to identify potential issues early and come up with test scenarios together. like pair testing/pair programing
-  Work with UX designers and infrastructure engineers for e.g test env.

---

## Assignment Part 2

### Question 3: Finding Incorrect Test Cases and Suggestions

#### **Incorrect Unit Test:**

```python
def test_add_item_empty_name():
    order = Order()
    order.add_item_to_order("", 1000, 2) # Incorrect behavior; no error is raised.
    assert len(order.items) == 0  # Fails because the item gets added.
```

**Issue:** The test does not expect an exception, even though an empty name should raise an error.

**Corrected Version:**

```python
import pytest

def test_add_item_empty_name():
    order = Order()
    with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
        order.add_item_to_order("", 1000, 2)
```

#### **Issue with Unit Test 2 may be not issue just a suggestion:**
Using `try-except` for validation is not best practice. Instead, `pytest.raises` provides cleaner exception handling.

#### **Incorrect Integration Test:**

```python
def test_calculate_total_after_invalid_addition():
    order = Order()
    try:
        order.add_item_to_order("Laptop", -1000, 2) # Invalid addition.
    except ValueError:
        pass
    assert order.calculate_total() == 0 # Incorrect assumption.
```
For me the assumption that an invalid item would still be added to the order is incorrect
I believe the test should verify that an invalid addition does not modify the order, instead of assuming the total becomes 0 so better approach is to check whether the order remains unchanged after an invalid addition.

**Corrected Version:**

```python
import pytest

def test_calculate_total_after_invalid_addition():
    order = Order()
    order.add_item_to_order("Mouse", 50, 1)
    with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
        order.add_item_to_order("Laptop", -1000, 2)
    assert order.calculate_total() == 50
```

---

### Additional Unit Test

#### **Test Name:** `test_add_item_negative_quantity`
**Description:** Ensures that adding an item with a quantity less than zero raises a `ValueError`.

```python
import pytest

def test_add_item_negative_quantity():
    order = Order()
    with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
        order.add_item_to_order("Laptop", 1000, -2)
```

**Note:** This case was not originally handled in the `Order` module.

#### **Test Name:** `test_add_item_non_string_name`
**Description:** Ensures that an item name must be a string.

```python
import pytest

def test_add_item_non_string_name():
    order = Order()
    with pytest.raises(ValueError, match="Invalid input: item_name must be a string"):
        order.add_item_to_order(123, 1000, 2)
```

---

### Additional Integration Test

#### **Test Name:** `test_calculate_total_with_multiple_invalid_additions`
**Description:** Ensures that multiple invalid additions do not affect the total calculation.

```python
import pytest

def test_calculate_total_with_multiple_invalid_additions():
    order = Order()
    order.add_item_to_order("Keyboard", 80, 1)  # Valid item
    
    invalid_items = [
        ("", 100, 1),     
        ("Monitor", -200, 1),  
        ("Headphones", 50, 0) 
    ]
    
    for item in invalid_items:
        with pytest.raises(ValueError, match="Invalid input: item_name must be non-empty, price and quantity must be greater than 0."):
            order.add_item_to_order(*item)
    
    assert order.calculate_total() == 80
```

---
