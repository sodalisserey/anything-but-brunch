from tabulate import tabulate
from datetime import datetime
import csv

def main():
    day_menu = get_menu("day_menu.csv")
    brunch_menu = get_menu("brunch_menu.csv")
    summer_menu = get_menu("summer_menu.csv")

    order_confirmed = False
    current_date_time = datetime.today().strftime("%A %d/%m/%y %H:%M")
    current_month = datetime.now().month
    order = {}

    name = input(f"\nWelcome to the Café! What is your name? ").strip().title()
    print(f"\nHello {name}! Check out our menu:\n{format_menu(day_menu, brunch_menu, summer_menu)}"
          f"\nPlease note brunch is served between 10:00-13:00"
          f"\nSummer items are served from June to September"
          f"\nEnter 'done' once you've completed your order!"
          f"\n")

    while not order_confirmed:
        current_time = datetime.today().strftime("%H:%M")
        request = input(f"What can I get you today, {name}? ").strip().title()
        order_valid = validate_order(day_menu, brunch_menu, summer_menu, request, current_time, current_month)
        order_confirmed = confirm_order(request, order)

        if order_valid:
            if request not in order:
                order.update({request: 0})
            order[request] += 1

    print(f"\nHere's your receipt, {name}:"
          f"\n{get_receipt(order, day_menu, brunch_menu, summer_menu, current_date_time)}"
          f"\nYour order should be with you shortly"
          f"\nWe hope to see you again soon ₊˚⊹♡")


def get_menu(menu_csv):
    menu = {}

    with open(menu_csv) as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = row["item"]
            price = float(row["price"])
            menu[item] = price

    return menu


def format_menu(day_menu, brunch_menu, summer_menu):
    formatted_menu = [["A L L - D A Y   M E N U", ""]] + \
                     [[f"{item}", f"£ {price:.2f}"] for item, price in day_menu.items()] + \
                     [["-------------------------", "-------"]] + \
                     [["B R U N C H   M E N U", ""]] + \
                     [[f"{item}", f"£ {price:.2f}"] for item, price in brunch_menu.items()] + \
                     [["-------------------------", "-------"]] + \
                     [["S U M M E R   M E N U", ""]] + \
                     [[f"{item}", f"£ {price:.2f}"] for item, price in summer_menu.items()]

    return tabulate(formatted_menu, headers=[], tablefmt="fancy_outline", colalign=("left", "right"))


def validate_order(day_menu, brunch_menu, summer_menu, request, current_time, current_month):
    order_valid = False
    if brunch_menu.get(request):
        if "10:00" > current_time or current_time > "13:00":
            print(f"Brunch? At {current_time}? Why don't we try again?")
        else:
            order_valid = True
    elif summer_menu.get(request):
        if current_month < 6 or current_month > 9:
            print("Nice try, but the summer menu is for summer...")
        else: order_valid = True
    elif day_menu.get(request):
        order_valid = True
    else:
        if request.lower() != "done":
            print("Good idea, but we're not serving that at the moment!")

    return order_valid


def confirm_order(request, order, answer=None):
    order_confirmed = False
    if request.lower() == "done":
        if order != {}:
            print(f"\nTo confirm, you would like:")
            for item in order:
                print(f"{order[item]} {item}")
            if not answer:
                answer = input("Would you like to proceed? (Y/N) ").strip().lower()
            if answer == "y" or answer == "yes":
                order_confirmed = True
        else:
            print("Please enter your order!")

    return order_confirmed


def get_receipt(order, day_menu, brunch_menu, summer_menu, current_datetime):
    total = 0
    menus = [[item, price] for item, price in day_menu.items()] + \
            [[item, price] for item, price in brunch_menu.items()] + \
            [[item, price] for item, price in summer_menu.items()]

    receipt = [[f"{current_datetime}", ""],
               ["-------------------------", "-------"],
               ["R E C E I P T", ""],
    ]

    for item, price in menus:
        for item_order in order:
            if item == item_order:
                item_total = float(price) * float(order[item_order])
                total += item_total
                receipt.append([f"x{order[item_order]} {item}", f"£ {item_total:.2f}"])

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