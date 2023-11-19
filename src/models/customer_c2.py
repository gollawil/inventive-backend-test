class CustomerC2:
    """
    A customer's customer, eg Luxe Pants (customer of Massive Clothing)
    """

    def __init__(self, **customer_attrs):
        self.name = customer_attrs.get("name")
        self.notifications_email = customer_attrs.get("notifications_email")

    def alerts(self):
        """
        Stub method.

        Return a list of alerts that the user has requested
        """

        return []
