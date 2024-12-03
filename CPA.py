from connection_pool import get_connection
import database
import prompts
import datetime as dt


class CPA:
    def __init__(self, first_name: str, last_name: str, email: str, license_num: str, license_expire: dt.date, _id: int = None):
        self.first_name = first_name,
        self.last_name = last_name,
        self.email = email,
        self.license_num = license_num,
        self.license_expire = license_expire,
        self.id = _id  # id set to none for now since it cannot be assigned until after it gets added to the database

    def __repr__(self):
        return f"CPA({self.first_name=} {self.last_name=} {self.email=} {self.license_num=} {self.license_expire=} {self.id=})"

    def save(self):
        with get_connection() as connection:
            new_cpa_id = database.insert_cpa(connection, self.first_name, self.last_name, self.email, self.license_num, self.license_expire)
            self.id = new_cpa_id

    # this function is just going to update the already existing row with the necessary information
    def submit_tax_return(self):
        current_time = dt.datetime.now()
        timestamp = current_time.timestamp()
        file_status = True
        CPA_check = True  # True because the CPA is the one submitting the tax return

        with get_connection() as connection:
            returns = database.get_all_returns(connection)
            for _return in returns:
                print(f"ID {_return[0]}: Tax Return for {_return[7]} {_return[8]}")
            return_id = int(input(prompts.RETURN_PROMPT))
            database.update_tax_return_cpa(connection, timestamp, file_status, CPA_check, self.id, return_id)
        print(f"\nSuccessfully submitted the tax return.\n")

    @classmethod
    def get(cls, cpa_id: int):
        with get_connection() as connection:
            try:
                cpa = database.get_cpa(connection, cpa_id)
                if cpa is None:  # if client ends up empty, throw an error since we can't create the Client object
                    raise AttributeError(f"There was no CPA found with ID {cpa_id}")
                return cls(cpa[1], cpa[2], cpa[3], cpa[4], cpa[5], cpa[0])
            except AttributeError as e:
                print(f"Error retrieving CPA information: {str(e)}")
