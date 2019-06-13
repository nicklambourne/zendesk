"""
Interactive command line interface for accessing tickets on the Zendesk API.
"""

from pyfiglet import Figlet
from getpass import getpass
from typing import List
from zenpy import Zenpy, ZenpyException
from zenpy.lib.exception import RecordNotFoundException


# Column sizes (assuming an 80 character width)
sizes = {
    "id": 8,
    "subject": 32,
    "user": 20,
    "date": 10,
    "time": 10
}


def pad(contents: str, size: int) -> str:
    """
    Pads text on the right to meet the target size, shortening if necessary.
    :param contents: the original content to left pad
    :param size: the target size
    :return: the original string contents padded with spaces on the right
    """
    if len(contents) < size:
        return f"{contents}{' ' * (size - len(contents))}"
    else:
        return f"{contents[:size-4]}... "


def line(id: str, subject: str, user: str, date: str, time: str) -> str:
    """
    Produces a formatted line of text containing the info for a ticket.
    :param id: ticket ID number
    :param subject: ticket subject text
    :param user: name of user who submitted the ticket
    :param date: date ticket was submitted
    :param time: time ticket was submitted
    :return: ticket summary string of exactly 80 characters in length
    """
    return f"{pad(id, sizes['id'])}" \
           f"{pad(subject, sizes['subject'])}" \
           f"{pad(user, sizes['user'])}" \
           f"{pad(date, sizes['date'])}" \
           f"{pad(time, sizes['time'])}"


def header() -> str:
    """
    Creates a header line for the tickets view.
    :return: string of column titles
    """
    return line("ID", "SUBJECT", "USER", "DATE", "TIME")


def get_tickets(client: Zenpy) -> List:
    """
    Gets all tickets from the Zendesk API for the workspace.
    N.B.: will be inefficient at large size, should paginate requests
    in future.
    :param client: the Zenpy client connection object
    :return: a list of all tickets for the client workspace
    """
    return list(client.tickets())


def tickets(client: Zenpy) -> None:
    """
    Interactive display of tickets (paginated).
    :param client: the Zenpy client connection object
    """
    print("Gathering tickets from Zendesk...")

    results = get_tickets(client)
    index = 0

    while True:
        first = max(index, 0)
        last = min(first + 4, len(results))

        print(header())

        for ticket in results[first:last+1]:
            print(line(str(ticket.id),
                       ticket.subject,
                       ticket.requester.name,
                       ticket.created.strftime("%m/%d/%y"),
                       ticket.created.strftime("%H:%M:%S")))

        print(f"Showing tickets {first + 1} to {last} of {len(results)}. "
              f"Type 'next', 'prev', or 'exit' to continue.")

        option = input()

        if option == "next":
            index = min(index + 5, len(results) - 5)
        elif option == "prev":
            index = max(0, index - 5)
        elif option == "exit":
            return
        else:
            print("Invalid option, try again.")


def sanitise_description(original: str) -> str:
    """
    Remove newlines from ticket descriptions.
    :param original: the string to sanitise
    :return: the same string, with newlines as spaces
    """
    return original.replace("\n", " ")


def display_ticket(number: str, client) -> None:
    """
    Displays detailed view of a single ticket
    :param number: the ID number of the ticket to display
    """
    try:
        ticket = client.tickets(id=number)
    except ZenpyException:
        print("Error accessing ticket with that ID. Are you sure it exists?")
        return
    print(f"{'*' * 80}\n"
          f"{pad('Ticket ID: ', 15)}{pad(str(ticket.id), 65)}\n"
          f"{pad('Subject: ', 15)}{pad(ticket.subject, 65)}\n"
          f"{pad('Description: ', 15)}{pad(sanitise_description(ticket.description), 65)}\n"
          f"{pad('Created: ', 15)}{pad(ticket.created_at, 65)}\n"
          f"{pad('Submitted by: ', 15)}{pad(ticket.submitter.name, 65)}\n"
          f"{pad('Status: ', 15)}{pad(ticket.status.capitalize(), 65)}\n"
          f"{'*' * 80}\n")


def main() -> None:
    """
    Runs the interactive client
    :return:
    """
    print(Figlet(font="slant").renderText("Zendesk"), end="")
    print("Welcome to the Zendesk ticket viewer!\n"
          "Enter your details below to log in.\n")

    email = input("Email: ")
    password = getpass()
    subdomain = input("Subdomain: ")

    try:
        print("\nConnecting to the Zendesk API...\n")
        client = Zenpy(email=email,
                       password=password,
                       subdomain=subdomain)

    except ZenpyException:
        print("Error connecting to the Zendesk service. Please try again.\n"
              "- Are your credentials correct?\n"
              "- Is your internet connection working?")
        return

    while True:
        print("\nChoose one of the following options to continue:\n"
              " ➥ tickets: to list all tickets\n"
              " ➥ <ticket_number>: to show details for the a single ticket\n"
              " ➥ exit: to leave the program")

        option = input()

        if option == "tickets":
            tickets(client)
        elif option == "exit":
            print("See you next time!")
            return
        else:
            try:
                ticket_number = str(int(option))
                display_ticket(ticket_number, client)
            except ValueError:
                print("Invalid Option")
            except RecordNotFoundException:
                print("Record Not Found")


if __name__ == "__main__":
    """
    Main event loop, for running as an independent script.
    """
    main()
