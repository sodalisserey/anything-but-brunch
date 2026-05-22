import pytest
from project import get_menu, format_menu, validate_order, confirm_order, get_receipt


def test_get_menu():
    """
    Test CSV menu files are correctly parsed into dictionaries
    """

    # Check invalid input type raises TypeError
    with pytest.raises(TypeError):
        get_menu(None)

    # Load real menu file
    menu = get_menu("day_menu.csv")

    # Verify return type is correct
    assert isinstance(menu, dict)

    # Verify menu is not empty
    assert len(menu) > 0

    # Verify structure of dictionary values
    for item, price in menu.items():
        assert isinstance(item, str)
        assert isinstance(price, float)


def test_format_menu():
    """
    Test that menu dictionaries are correctly formatted into a string table
    """

    # Check invalid input type raises TypeError
    with pytest.raises(TypeError):
        format_menu(None)

    # Create mock menus for testing
    day = {"Coffee": 3.00}
    brunch = {"Toast": 5.00}
    summer = {"Lemonade": 4.50}

    # Generate formatted menu string
    menu = format_menu(day, brunch, summer)

    # Ensure output is a string
    assert isinstance(menu, str)

    # Check that all menu items appear in output
    assert "Coffee" in menu
    assert "Toast" in menu
    assert "Lemonade" in menu


def test_validate_order():
    """
    Test that validation works correctly based on availability rules (time and seasonal restrictions)
    """

    # Check invalid input type raises TypeError
    with pytest.raises(TypeError):
        validate_order(None)

    # Create mock menus for testing
    day = {"Coffee": 3.00}
    brunch = {"Toast": 5.00}
    summer = {"Affogato": 4.50}

    # Valid day menu item should be accepted
    assert validate_order(day, brunch, summer,
                          "Coffee", "12:00", 7) is True

    # Invalid menu item should be rejected
    assert validate_order(day, brunch, summer,
                          "Pizza", "12:00", 7) is False

    # Brunch item should be rejected if not within rules
    assert validate_order(day, brunch, summer,
                          "Toast", "15:00", 7) is False

    # Summer item should be rejected if not within rules
    assert validate_order(day, brunch, summer,
                          "Affogato", "15:00", 2) is False


def test_confirm_order():
    """
    Test order confirmation logic when customer finishes ordering
    """

    # Check invalid input type raises TypeError
    with pytest.raises(TypeError):
        confirm_order(None)

    # If "done" followed by "y" order should be confirmed
    assert confirm_order("done", {"Muffin": 1}, "y") is True

    # If "done" followed by "n" order should not be confirmed
    assert confirm_order("done", {"Muffin": 1}, "n") is False

    # Empty order should not be confirmed
    assert confirm_order("done", {}, "y") is False

    # If not "done" order should not be confirmed
    assert confirm_order("Coffee", {"Muffin": 1}, "y") is False


def test_get_receipt():
    """
    Test receipt generation including totals costs, service fee and formatting
    """

    # Check invalid input type raises TypeError
    with pytest.raises(TypeError):
        get_receipt(None)

    # Mock order matching menu item
    order = {"Coffee": 2}
    day = {"Coffee": 3.00}
    brunch = {}
    summer = {}

    # Generate receipt
    receipt = get_receipt(order, day, brunch, summer,"Thursday 12/12/24 16:00")

    # Verify output type
    assert isinstance(receipt, str)

    # Check key information appears in receipt
    assert "Coffee" in receipt
    assert "£ 6.00" in receipt
    assert "Service Fee" in receipt
    assert "Total" in receipt