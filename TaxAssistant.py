import prompts
from connection_pool import get_connection
import database
import datetime as dt

# at first, I just wanted to make this a simple function but it made a little more sense to
# add tax assistant class. Makes sense for the future if the assistant has to take on more responsibilities
# since you could add more attributes and methods that handle the new tasks
# for now, it'll just have one method, to turn in the clients materials if the cpa hasn't


class TaxAssistant:
    def __init__(self, first_name: str, last_name: str, _id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.id = _id

    def __repr__(self):
        return f"{self.first_name=} {self.last_name=} {self.id=}"

    def save(self):
        with get_connection() as connection:
            assist_id = database.insert_assistant(connection, self.first_name, self.last_name)
            self.id = assist_id

    # this function is just going to update the already existing row with the necessary information
    def submit_tax_return(self):
        current_time = dt.datetime.now()
        timestamp = current_time.timestamp()
        CPA_check = False  # false because the assistant is turning it in
        file_status = True

        # to update the tax return I need the id, this was a quick way to show the user the IDs and then update
        with get_connection() as connection:
            returns = database.get_all_returns(connection)
            for _return in returns:
                print(f"ID {_return[0]}: Tax Return for {_return[7]} {_return[8]}")
            return_id = int(input(prompts.RETURN_PROMPT))
            database.update_tax_return_assistant(connection, timestamp, file_status, CPA_check, self.id, return_id)
        print(f"\nSuccessfully submitted the tax return.\n")

    @classmethod
    def get(cls, assistant_id):
        with get_connection() as connection:
            try:
                assistant = database.get_assistant(connection, assistant_id)
                if assistant is None:  # if client ends up empty, throw an error since we can't create the Client object
                    raise AttributeError(f"There was no assistant found with ID {assistant_id}")
                return cls(assistant[1], assistant[2], assistant[0])
            except AttributeError as e:
                print(f"Error retrieving assistant information: {str(e)}")





