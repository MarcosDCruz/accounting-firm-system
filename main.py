from connection_pool import get_connection
import datetime as dt
import database
import prompts

from Models.Client import Client
from Models.CPA import CPA
from Models.TaxAssistant import TaxAssistant


def add_new_client():
    first_name, last_name = input("What is your first and last name?\n").split(" ")
    address, city, state = input("What is your address? (ex. 123 Street Name,City,ST)\n").split(",")
    income = input("What is your reported annual income? (No need to add $ symbol)\n")
    provided_materials = False
    client = Client(first_name, last_name, address, city, state, income, provided_materials)
    client.assign_cpa()
    client.save()


def add_tax_assistant():
    first_name, last_name = input("What is your first and last name?\n").split()
    assistant = TaxAssistant(first_name, last_name)
    assistant.save()


def add_new_cpa():
    first_name, last_name = input("What is your first and last name?\n").split()
    email = input("What is your company assigned email?\n")
    license_number = input("Please enter your license number:\n")

    # need to get date as str and then convert to date object
    license_expiration = input("Please enter the date your license expires (MM/DD/YYYY):\n")  # make this disgusting
    license_expiration_date = dt.datetime.strptime(license_expiration, '%m/%d/%Y')

    cpa = CPA(first_name, last_name, email, license_number, license_expiration_date)
    cpa.save()


def prompt_client_materials():
    selection = input(prompts.CLIENT_MATERIALS_PROMPT)
    client_id = int(input(prompts.CLIENT_PROMPT))
    client = Client.get_materials_status(client_id)

    if selection == "1":
        if client.provided_materials:  # provided_materials is a bool type
            print(f"\n{client.first_name} {client.last_name} has provided the required materials.\n")
        else:
            print(f"\n{client.first_name} {client.last_name} has not provided the required materials.\n")
    elif selection == "2":
        if client.provided_materials:
            print(f"\nYou have already submitted the required materials.\n")
        else:
            client.provided_materials = True
            print(f"\nThank you {client.first_name}, you have submitted your materials.\n")  # i love vague statements
    else:
        print("Invalid option.")


def prompt_tax_return():
    selection = input(prompts.TAX_RETURN_PROMPT)
    if selection == "1":
        client_id = int(input(prompts.CLIENT_PROMPT))
        client = Client.get_materials_status(client_id)
        client.check_return_status()
    elif selection == "2":
        role_selection = input(prompts.CPA_ASSISTANT_PROMPT)
        if role_selection == "1":
            cpa_id = int(input(prompts.CPA_PROMPT))
            cpa = CPA.get(cpa_id)
            cpa.submit_tax_return()
        elif role_selection == "2":
            assistant_id = int(input(prompts.ASSISTANT_PROMPT))
            assistant = TaxAssistant.get(assistant_id)
            assistant.submit_tax_return()
        else:
            print("Invalid option.")
    else:
        print("Invalid option.")


MENU_OPTIONS = {
    "1": add_new_client,
    "2": add_tax_assistant,
    "3": add_new_cpa,
    "4": prompt_client_materials,
    "5": prompt_tax_return,
}


def menu():
    with get_connection() as connection:
        database.create_tables(connection)

    while (menu_selection := input(prompts.MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[menu_selection]()
        except KeyError:
            print("\nNot a valid option. Please input a valid option provided by the menu.\n")


if __name__ == "__main__":
    menu()
