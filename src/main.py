from getpass import getpass
from typing import List
from zenpy import Zenpy, ZenpyException



# Column sizes (assuming an 80 char width)
sizes = {
    "id": 8,
    "subject": 32,
    "user": 20,
    "date": 10,
    "time": 10
}


def pad(contents: str, size: int) -> str:
    """

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

    :param id:
    :param subject:
    :param user:
    :param date:
    :param time:
    :return:
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

    :param client: the Zenpy client connection object
    :return: a list of all tickets for the client
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
        print(f"Showing tickets {first} to {last} of {len(results)}. "
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


def display_ticket(number: int) -> None:
    pass


def main() -> None:
    """

    :return:
    """
    print("Welcome to the Zendesk ticket viewer!")

    email = input("Email: ")
    password = getpass()
    subdomain = input("Subdomain: ")

    try:
        print("Connecting to the Zendesk API...")
        client = Zenpy(email=email,
                       password=password,
                       subdomain=subdomain)

    except ZenpyException:
        print("Error connecting to the Zendesk service. Please try again\n"
              "- Are your credentials correct?\n"
              "- Is your internet connection ")

    while True:
        print("Choose one of the following options:\n"
              "tickets: to list all tickets\n"
              "<ticket_number>: to show details for the given ticket")

        option = input()

        if option == "tickets":
            tickets(client)
        else:
            try:
                ticket_number = int(option)
                display_ticket(ticket_number)
            except ValueError:
                print("Invalid Option")


if __name__ == "__main__":
    main()
