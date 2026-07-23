import sys
import argparse
from dotenv import load_dotenv
from bot.client import BinanceBot

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console(color_system=None)


def get_valid_input(prompt: str, valid_options: list = None, input_type=str, min_val=None):

    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                console.print("  Input cannot be empty. Please try again.")
                continue

            val = input_type(user_input)

            if input_type == str and valid_options:
                val = val.upper()
                if val not in valid_options:
                    console.print(f"  Invalid option. Please choose from: {', '.join(valid_options)}")
                    continue

            if input_type == float and min_val is not None:
                if val <= min_val:
                    console.print(f"  Value must be greater than {min_val}.")
                    continue

            return val
        except ValueError:
            console.print(f"  Invalid format. Please enter a valid {input_type.__name__}.")


def print_header():
    console.print(Panel.fit("Binance Futures Trading Bot", box=box.DOUBLE))


def print_menu():
    table = Table(title="Main Menu", box=box.SQUARE, show_header=True)
    table.add_column("Option", justify="center")
    table.add_column("Action")
    table.add_row("1", "Place MARKET Order")
    table.add_row("2", "Place LIMIT Order")
    table.add_row("3", "Exit")
    console.print(table)


def print_order_request(symbol, side, order_type, quantity, price):
    table = Table(title="Order Request", box=box.SQUARE, show_header=False)
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    table.add_row("Price", str(price) if price is not None else "- (market price)")
    console.print(table)


def print_order_result(response):
    table = Table(title="Order Result - SUCCESS", box=box.SQUARE, show_header=False)
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Order ID", str(response.get("orderId")))
    table.add_row("Status", str(response.get("status")))
    table.add_row("Symbol", str(response.get("symbol")))
    table.add_row("Side", str(response.get("side")))
    table.add_row("Type", str(response.get("type")))
    table.add_row("Executed Qty", str(response.get("executedQty", "N/A")))
    table.add_row("Avg Price", str(response.get("avgPrice", "N/A")))
    console.print(table)
    console.print("(Check trading_bot.log for full details)")
    console.rule()


def print_error(message):
    console.print(Panel.fit(f"Order Failed\n\n{message}", box=box.SQUARE, title="Error"))
    console.print("(Check trading_bot.log for full details)")
    console.rule()


def interactive_mode():
    """Runs the interactive CLI wizard with menus and prompts."""
    print_header()

    try:
        bot = BinanceBot()
    except Exception as e:
        print_error(f"Failed to initialize bot: {e}")
        return

    while True:
        print_menu()
        choice = input("\nSelect an option (1-3): ").strip()

        if choice == '3':
            console.print("Exiting... Goodbye!")
            break
        elif choice not in ['1', '2']:
            console.print("  Invalid choice. Please enter 1, 2, or 3.")
            continue

        order_type = "MARKET" if choice == '1' else "LIMIT"

        console.print(f"\n-- Placing {order_type} Order --")
        symbol = get_valid_input("Enter Symbol (e.g., BTCUSDT): ", input_type=str)
        side = get_valid_input("Enter Side (BUY or SELL): ", valid_options=["BUY", "SELL"])
        quantity = get_valid_input("Enter Quantity: ", input_type=float, min_val=0)

        price = None
        if order_type == "LIMIT":
            price = get_valid_input("Enter Limit Price: ", input_type=float, min_val=0)

        print_order_request(symbol, side.upper(), order_type, quantity, price)
        console.print("\nSubmitting order to Binance Testnet...")

        try:
            response = bot.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
            print_order_result(response)

        except Exception as e:
            print_error(str(e))


def main():
    # Load environment .envs
    load_dotenv()

    # If arguments are passed, use argparse mode
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Simplified Trading Bot for Binance Futures Testnet")
        parser.add_argument("symbol", help="Trading pair symbol, e.g., BTCUSDT")
        parser.add_argument("side", choices=["BUY", "SELL"], type=str.upper, help="BUY or SELL")
        parser.add_argument("order_type", choices=["MARKET", "LIMIT"], type=str.upper, help="MARKET or LIMIT")
        parser.add_argument("quantity", type=float, help="Amount to trade")
        parser.add_argument("--price", "-p", type=float, help="Price (required for LIMIT orders)")

        args = parser.parse_args()

        print_header()
        try:
            bot = BinanceBot()
            print_order_request(args.symbol.upper(), args.side, args.order_type, args.quantity, args.price)
            console.print("\nSubmitting order to Binance Testnet...")
            response = bot.place_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.order_type,
                quantity=args.quantity,
                price=args.price
            )
            print_order_result(response)
        except Exception as e:
            print_error(str(e))
    else:
        # If no argue pass lucnh c
        interactive_mode()


if __name__ == "__main__":
    main()