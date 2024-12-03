from connection_pool import get_connection
import database
import datetime as dt


class Client:
    def __init__(self, first_name: str, last_name: str, address: str, city: str, state: str, income: str, _provided_materials: bool, _id: int = None, cpa_id: int = None):
        self.id = _id,  # underscore because id is python keyword
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.income = income
        self._provided_materials = _provided_materials
        self.cpa_id = cpa_id

    def __repr__(self):  # added {self.attribute=} so it would list the attribute and its current value
        return f"Client({self.id=} {self.first_name=} {self.last_name=} {self.address=} {self.city=} {self.state=} {self.income=} {self.provided_materials=} {self.cpa_id=})"

    def save(self):
        with get_connection() as connection:
            new_client_id = database.insert_client(connection, self.first_name, self.last_name, self.address, self.city, self.state, self.income, self.provided_materials, self.cpa_id)
            self.id = new_client_id

            # creating the initial row for the tax return since we also need to track that it has not been filed
            # timestamp and the 3 possible associated ids won't be stored here since the tax returned isn't filed
            timestamp = None  # 0 since I can't store None
            file_status = False
            cpa_check = False
            assistant_id = None
            cpa_id = None

            database.insert_tax_return(connection, timestamp, file_status, cpa_check, new_client_id, assistant_id, cpa_id)

    def assign_cpa(self):
        with get_connection() as connection:
            CPA_id = database.get_random_cpa(connection)
            self.cpa_id = CPA_id  # does this make clients dependent on CPAs?

    def check_return_status(self):
        with get_connection() as connection:
            client_return = database.get_client_return(connection, self.id)
            if client_return is None:  # this check might be redundant since the getter already checks and then this func is called
                print(f"\nThere is no client with that ID.\n")
            elif client_return[4]:
                timestamp_date = dt.datetime.fromtimestamp(client_return[3])
                formatted_date = dt.datetime.strftime(timestamp_date, "%m/%d/%Y")
                print(f"\n{self.first_name} {self.last_name} filed their tax return on {formatted_date}.", end=" ")
                if client_return[5]:
                    print(f"It was checked by CPA {client_return[7]} {client_return[8]}.\n")
                else:
                    print(f"It was filed by an assistant, but has not been checked by a CPA.\n")
            else:
                print(f"\n{self.first_name} {self.last_name} has not filed their tax return.\n")

    @property
    def provided_materials(self):
        return self._provided_materials

    @provided_materials.setter
    def provided_materials(self, status: bool):
        if status:
            self._provided_materials = status
            with get_connection() as connection:
                database.update_client_materials(connection, status, self.id)
        else:
            print(f"Somehow an error occurred.")

    @classmethod
    def get_materials_status(cls, client_id: int):
        with get_connection() as connection:
            try:
                client = database.get_client(connection, client_id)
                if client is None:  # if client ends up empty, throw an error since we can't create the Client object
                    raise AttributeError(f"There was no client found with ID {client_id}")
                return cls(client[1], client[2], client[3], client[4], client[5], client[6], client[7], client[0], client[8])
            except AttributeError as e:
                print(f"Error retrieving client information: {str(e)}")
# I can't get the interpreter to stop throwing its own AttributeError


