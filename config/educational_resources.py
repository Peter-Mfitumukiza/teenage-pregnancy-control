# def show_menu():
#     print("Welcome to the Educational Resources Section!")
#     print("Choose a topic to learn about:")
#     print("1. Reproductive Health")
#     print("2. Pregnancy Risk")
#     print("3. Contraceptive Methods")
#     print("4. Pre-wedding Advice")
#     print("5. STDs")
#     print("0. Exit")

# def show_lesson(choice):
#     lessons = {
#         "1": "Reproductive Health is about maintaining your body’s health during all stages of life...",
#         "2": "Pregnancy Risk increases with unprotected sex. Learn how to protect yourself...",
#         "3": "Contraceptive Methods include pills, condoms, implants, and more. Choose what fits your lifestyle...",
#         "4": "Pre-wedding Advice includes health checks, open conversations, and readiness for partnership...",
#         "5": "STDs are infections passed through sexual contact. Always stay informed and protected..."
#     }

#     if choice in lessons:
#         print("\n" + lessons[choice])
#     else:
#         print("Invalid choice. Please select a valid option.")

# def main():
#     while True:
#         show_menu()
#         user_input = input("Enter the number of your choice: ")
#         if user_input == "0":
#             print("Thanks for learning! Stay safe ")
#             break
#         else:
#             show_lesson(user_input)
#             print("\n--------------------\n")

# if __name__ == "__main__":
#     main()
