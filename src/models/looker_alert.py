from datetime import datetime, timedelta


class LookerAlert:

    FREQUENCIES = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
    }

    def __init__(
        self,
        customer_c2,
        query_settings,
        alert_settings,
    ):
        self.customer_c2 = customer_c2

        self.model = query_settings["model"]
        self.view = query_settings["view"]
        self.fields = query_settings["fields"]
        self.filters = query_settings["filters"]

        self.email = alert_settings.get(
            "email",
            self.customer_c2.notifications_email,
        )
        self.frequency = alert_settings["frequency"]
        self.last_checked = None

    def request_body(self):
        return {
            "model": self.model,
            "view": self.view,
            "fields": self.fields,
            "filters": self.filters,
        }

    def should_check(self):
        """
        Determine if this alert should be run,
        based on when it was last run.
        """

        if self.last_checked is not None:
            time_to_compare = datetime.now() - timedelta(
                days=self.FREQUENCIES[self.frequency],
            )

            if time_to_compare <= self.last_checked:
                return False

        return True

    def update_last_checked(self):
        """
        Stub method.

        This should persist last_checked for future runs,
        for now it will just be stored in memory.
        """

        self.last_checked = datetime.now()
