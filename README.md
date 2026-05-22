# Anything But Brunch

### _Description_
Anything But Brunch is a 24-hour café simulation run by a domineering clock. It presents users with three different menus, allowing them to order items only when they are available according to the time of day or season. 
- Brunch menu items are only available between 10:00-13:00
- Summer menu items are only available from June to September
- Standard menu items are available at all times
  
After the user enters their items and confirms that the order is complete, an itemised receipt is generated, showing the date and time of purchase, all ordered items, a 10% service fee charge and the total cost.

### _Features_
- Dynamic menu availability based on real-world date and time
- CSV menus for easy customisation
- Formatted menus and receipts using tabulate
- Unit testing with `pytest`

### _Main File_
#### ```src/anything_but_brunch.py``` <br>
Contains the main programme logic, including all five core functions and the main() function.
The programme runs inside a while loop that:
1. Prompts the user for an order
2. Validates the request
3. Updates the order dictionary
4. Confirms completion
5. Generates a receipt

### _Functions_
#### ``` get_menu(menu_csv) ``` <br>
Reads menu data from CSV files using `csv.DictReader()` and returns a dictionary containing menu items and prices.

#### ```format_menu(standard_menu, brunch_menu, summer_menu)``` <br>
Compiles menu dictionaries before formatting them using `tabulate`.

#### ```validate_order(standard_menu, brunch_menu, summer_menu, request, current_time)``` <br>
Validates user order requests by checking whether:
- Item exists;
- Brunch menu items are ordered during valid hours
- Summer menu items are ordered during valid months

If valid, the function returns `True`, allowing the item to be added to the order dictionary.

#### ```confirm_order(request, order, answer)``` <br>
Checks whether the user entered `"done"` and prompts order confirmation
If the user confirms with `"yes"`, the function returns `True`, allowing the programme to exit the ordering loop.

#### ```get_receipt(standard_menu, brunch_menu, summer_menu, order, current_datetime)``` <br>
Calculates:
- Item totals
- 10% service fee
- Grand total
  
Then generates a receipt containing the ordering date and time, formatted using `tabulate`.

### _Supplementary Files_
#### ```tests/test_anything_but_brunch.py``` <br>
Contains unit tests for all five functions using pytest.

#### ```data/day_menu.csv``` <br>
Contains standard menu items with prices.

#### ```data/brunch_menu.csv``` <br>
Contains brunch menu items with prices.

#### ```data/summer_menu.csv``` <br>
Contains summer menu items with prices.

#### ```requirements.txt``` <br>
Lists all required installable ```Python``` packages.

### _Future Improvements_
Potential future features include
- Removing items from an order
- Removing service fee charge from receipt
- GUI or web interface implementation
