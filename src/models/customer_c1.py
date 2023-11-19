class CustomerC1:
    """
    A customer of Inventive, eg Massive Clothing
    """

    @classmethod
    def all(cls):
        """
        Stub method.

        A proper implementation would fetch all customers,
        most likely from a database.
        """

        return []

    def __init__(self, **customer_attrs):
        self.name = customer_attrs.get("name")

    def customers(self):
        """
        Stub method.

        A proper implementation would fetch all (C2) customers
        belonging to this customer, most likely from a database.
        """

        return []
