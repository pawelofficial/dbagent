"""
Runs the full sequence diagram flow:

  Waiter  greets  Client
  Client  greets  Waiter
  Client  selects Item (pizza)
  Client  adds item to Order
  Client  places order with Waiter
  Waiter  checks availability via Inventory
  Waiter  executes order
  Waiter  confirms to Client
  Client  asks for check
  Waiter  calculates check via Menu
  Waiter  gives check to Client
"""

from models import Client, Inventory, Item, Menu, Order, Waiter


def run() -> None:
    pizza = Item("pizza", price=12.50, availability=True)
    pasta = Item("pasta", price=9.00, availability=True)
    sushi = Item("sushi", price=15.00, availability=False)

    inventory = Inventory([pizza, pasta, sushi])
    menu = Menu({"pizza": 12.50, "pasta": 9.00, "sushi": 15.00})

    waiter = Waiter("Mario")
    client = Client("Alice")

    print("=" * 40)
    print("GREETINGS")
    waiter.greets(client)
    client.greets(waiter)

    print("-" * 40)
    print("ORDERING")
    selected = client.orders_item(pizza)
    order = Order()
    order.add_item(selected)
    
    selected = client.orders_item(pasta)
    order.add_item(selected)



    print("-" * 40)
    print("PLACING ORDER")
    client.place_order(order, waiter)

    print("-" * 40)
    print("CHECKING AVAILABILITY & EXECUTING")
    confirmed = waiter.execute_order(order, inventory)

    print("-" * 40)
    print("CONFIRMATION")
    waiter.confirm(client, confirmed)

    print("-" * 40)
    print("CHECK & PAYMENT")
    client.ask_for_check(waiter)
    check = waiter.prepare_check(order, menu)
    waiter.give_check(client, check)
    print("=" * 40)


if __name__ == "__main__":
    run()
