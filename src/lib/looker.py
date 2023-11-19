import looker_sdk
from dotenv import load_dotenv


class Looker:
    """
    A class responsible for interfacing with Looker
    """

    def __init__(self):
        load_dotenv()

        self.sdk = looker_sdk.init40()

    def query(self, request_body):
        """
        Stub method.

        A proper implementation would use a request body
        conforming to the looker_sdk API and return an object
        of some sort.

        The sample query provided in the example code returns a string;
        I could json.loads that and work with that, though I imagine Looker
        has an alternative method available that uses types they have defined
        """

        return []
