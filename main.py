import logging

from pos_logic import (
    DRINK_MENU,
    current_order,
    add_to_order,
    calculate_total,
    ItemNotFoundError,
    InvalidQuantityError
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def show_menu():
    print("\n========== HIGHLANDS MINI POS ==========")
    print("1. Xem thực đơn")
    print("2. Thêm món vào giỏ")
    print("3. Xem giỏ hàng & Tính tổng tiền")
    print("4. Thanh toán & Xóa giỏ hàng")
    print("5. Thoát ca làm việc")
    print("========================================")


def view_drink_menu():
    print("\n--- THỰC ĐƠN HIGHLANDS COFFEE ---")

    for code, info in DRINK_MENU.items():
        print(
            f"[{code}] - "
            f"{info['name']} - "
            f"{info['price']:,} VNĐ"
        )


def handle_add_order():
    print("\n--- THÊM MÓN VÀO GIỎ ---")

    try:
        drink_code = input(
            "Nhập mã đồ uống: "
        )

        quantity = int(
            input("Nhập số lượng: ")
        )

        add_to_order(
            drink_code,
            quantity
        )

        code = drink_code.strip().upper()

        print(
            f"Đã thêm {quantity} x "
            f"{DRINK_MENU[code]['name']} "
            f"vào giỏ hàng."
        )

    except ValueError:
        print(
            "Vui lòng nhập số lượng là một số nguyên!"
        )

        logging.error(
            "ValueError - Invalid quantity input"
        )

    except ItemNotFoundError:
        print(
            "Mã đồ uống không hợp lệ, vui lòng kiểm tra lại thực đơn!"
        )

        logging.warning(
            f"ItemNotFoundError - Code: "
            f"{drink_code.strip().upper()}"
        )

    except InvalidQuantityError:
        print(
            "Số lượng phải lớn hơn 0!"
        )

        logging.warning(
            f"InvalidQuantityError - Quantity: {quantity}"
        )


def view_order():
    if not current_order:
        print(
            "Giỏ hàng trống, vui lòng chọn món (Chức năng 2)."
        )
        return

    print("\n--- GIỎ HÀNG HIỆN TẠI ---")
    print(
        "Mã SP | Tên đồ uống          | Đơn giá  | Số lượng | Thành tiền"
    )
    print("-" * 64)

    for item in current_order:
        code = item["code"]
        quantity = item["quantity"]

        name = DRINK_MENU[code]["name"]
        price = DRINK_MENU[code]["price"]

        amount = price * quantity

        print(
            f"{code:<5} | "
            f"{name:<20} | "
            f"{price:>8,} | "
            f"{quantity:^8} | "
            f"{amount:>10,} VNĐ"
        )

    print("-" * 64)

    total = calculate_total(current_order)

    print(
        f"Tổng tiền cần thanh toán: "
        f"{total:,} VNĐ"
    )


def checkout():
    if not current_order:
        print(
            "Giỏ hàng trống, vui lòng chọn món (Chức năng 2)."
        )
        return

    total = calculate_total(current_order)

    print("\n--- THANH TOÁN ---")
    print(
        f"Tổng tiền cần thanh toán: "
        f"{total:,} VNĐ"
    )

    choice = input(
        f"Xác nhận thanh toán {total:,} VNĐ? (y/n): "
    ).lower()

    if choice == "y":
        logging.info(
            "Checkout successful"
        )

        current_order.clear()

        print("Thanh toán thành công.")
        print("Giỏ hàng đã được làm trống.")

    elif choice == "n":
        print(
            "Đã hủy thao tác thanh toán. Quay lại menu chính."
        )

    else:
        print(
            "Lựa chọn không hợp lệ. Thanh toán đã bị hủy."
        )


def main():
    while True:
        show_menu()

        choice = input(
            "Chọn chức năng (1-5): "
        )

        match choice:
            case "1":
                view_drink_menu()

            case "2":
                handle_add_order()

            case "3":
                view_order()

            case "4":
                checkout()

            case "5":
                logging.info(
                    "Cashier logged out. System shutdown."
                )

                print(
                    "Đã thoát ca làm việc. Hẹn gặp lại!"
                )

                break

            case _:
                print(
                    "Lựa chọn không hợp lệ!"
                )


if __name__ == "__main__":
    main()