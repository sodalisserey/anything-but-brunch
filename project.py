from tabulate import tabulate
from datetime import datetime
import csv

def main():
    """
    Run the café simulation which loads menu data from CSV files, display menus and ordering instructions, prompt the
    customer to order, validates availability of item requested, confirms finished order and prints a receipt
    """
    # Load menus from csv files
    day_menu = get_menu("day_menu.csv")
    brunch_menu = get_menu("brunch_menu.csv")
    summer_menu = get_menu("summer_menu.csv")

    # Get customer name
    order_confirmed = False
    current_date_time = datetime.today().strftime("%A %d/%m/%y %H:%M")
    current_month = datetime.now().month
    order = {}

    # Display formatted menus and ordering instructions
    name = input(f"\nWelcome to the Café! What is your name? ").strip().title()
    print(f"\nHello {name}! Check out our menu:\n{format_menu(day_menu, brunch_menu, summer_menu)}"
          f"\nPlease note brunch is served between 10:00-13:00"
          f"\nSummer items are served from June to September"
          f"\nEnter 'done' once you've completed your order!"
          f"\n")

    # Main ordering loop
    while not order_confirmed:
        current_time = datetime.today().strftime("%H:%M")

        # Prompt the customer to order
        request = input(f"What can I get you today, {name}? ").strip().title()

        # Check whether requested item can be ordered
        order_valid = validate_order(day_menu, brunch_menu, summer_menu, request, current_time, current_month)

        # Check whether customer wants to finish ordering
        order_confirmed = confirm_order(request, order)

        # Add valid request to order dictionary
        if order_valid:
            if request not in order:
                order.update({request: 0})
            order[request] += 1

    # Print final receipt
    print(f"\nHere's your receipt, {name}:"
          f"\n{get_receipt(order, day_menu, brunch_menu, summer_menu, current_date_time)}"
          f"\nYour order should be with you shortly"
          f"\nWe hope to see you again soon ₊˚⊹♡")


def get_menu(menu_csv: str) -> dict[str, float]:
    """
    Read menu items and prices from a csv file and return a dictionary containing items as keys and prices as float values
    """
    menu = {}

    with open(menu_csv) as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = row["item"]
            price = float(row["price"])
            menu[item] = price

    return menu


def format_menu(day_menu: dict[str, float], brunch_menu: dict[str, float], summer_menu: dict[str, float]) -> str:
    """
    Compile and format all menu dictionaries, using tabulate to return menus in a stylised string
    """
    formatted_menu = [["A L L - D A Y   M E N U", ""]] + \
                     [[f"{item}", f"£ {price:.2f}"] for item, price in day_menu.items()] + \
                     [["-------------------------", "-------"]] + \
                     [["B R U N C H   M E N U", ""]] + \
                     [[f"{item}", f"£ {price:.2f}"] for item, price in brunch_menu.items()] + \
                     [["-------------------------", "-------"]] + \
                     [["S U M M E R   M E N U", ""]] + \
                     [[f"{item}", f"£ {price:.2f}"] for item, price in summer_menu.items()]

    return tabulate(formatted_menu, headers=[], tablefmt="fancy_outline", colalign=("left", "right"))


def validate_order(day_menu: dict, brunch_menu: dict, summer_menu: dict, request: str,
        current_time: str, current_month: int) -> bool:
    """
    Check against several menu dictionaries to determine whether a requested item is available at current time and date
    (brunch items only available between 10:00 and 13:00, summer items only available from June to September) and
    return a boolean value
    """
    order_valid = False

    # Validate brunch items
    if brunch_menu.get(request):
        if "10:00" > current_time or current_time > "13:00":
            print(f"Brunch? At {current_time}? Why don't we try again?")
        else:
            order_valid = True

    # Validate summer items
    elif summer_menu.get(request):
        if current_month < 6 or current_month > 9:
            print("Nice try, but the summer menu is for summer...")
        else: order_valid = True

    # Validate all-day items
    elif day_menu.get(request):
        order_valid = True

    # Invalid items
    else:
        if request.lower() != "done":
            print("Good idea, but we're not serving that at the moment!")

    return order_valid

def confirm_order(request: str, order: dict, answer: str | None = None) -> bool:
    """
    Confirm whether the customer wants to complete their order when they input "done" in request and "y" in answer
    and return a boolean value
    """
    order_confirmed = False

    # When the customer enters done
    if request.lower() == "done":
        if order != {}:
            print(f"\nTo confirm, you would like:")
            for item in order:
                print(f"{order[item]} {item}")
            if not answer:
                answer = input("Would you like to proceed? (Y/N) ").strip().lower()
            if answer == "y" or answer == "yes":
                order_confirmed = True

        # If the customer has not ordered any items
        else:
            print("Please enter your order!")

    return order_confirmed


def get_receipt(order: dict, day_menu: dict, brunch_menu: dict, summer_menu: dict, current_datetime: str) -> str:
    """
    Generate a formatted receipt from a completed order dictionary, calculate the grand total from item prices
    in menu dictionaries with a 10% service fee and return a stylised string formatted by tabulate
    """
    total = 0

    # Combine all menus into one list
    menus = [[item, price] for item, price in day_menu.items()] + \
            [[item, price] for item, price in brunch_menu.items()] + \
            [[item, price] for item, price in summer_menu.items()]

    receipt = [[f"{current_datetime}", ""],
               ["-------------------------", "-------"],
               ["R E C E I P T", ""],
    ]

    # Calculate total price for ordered items
    for item, price in menus:
        for item_order in order:
            if item == item_order:
                item_total = float(price) * float(order[item_order])
                total += item_total
                receipt.append([f"x{order[item_order]} {item}", f"£ {item_total:.2f}"])

    # Calculate service fee and grand total
    service_fee = total * 0.1
    grand_total = total + service_fee

    receipt.append(["-------------------------", "-------"])
    receipt.append(["Service Fee", f"£ {service_fee:.2f}"])
    receipt.append(["Total", f"£ {grand_total:.2f}"])
    receipt.append(["-------------------------", "-------"])
    receipt.append(["Thank you for your visit! ", ""])

    return tabulate(receipt, headers=[], tablefmt="fancy_outline", colalign=("left", "right"))


if __name__ == "__main__":
    main()