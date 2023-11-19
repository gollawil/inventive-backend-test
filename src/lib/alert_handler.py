import models
from lib.looker import Looker


class AlertHandler:
    """
    A class responsible for sending notifications to customers that have
    requested them.

    This is set up with the intention that there could multiple other
    possible data sources the alerts are defined on.

    Only Looker is defined for now.
    """

    def __init__(self):
        # This is just a small optimization in the case of
        # having multiple Looker alerts requested.
        self.looker = None

        # This init method would be extended similarly if
        # implementing alerts from other third party integrations

    def execute(self, alerts):
        """
        This is the heart of the AlertHandler; for each alert supplied it:
        * checks if the alert should run (logic implemented per alert type)
        * queries for the data the alert is requesting
        * sends the notification
        """

        executed = []
        for alert in alerts:
            if alert.should_check():
                results = self._check_alert(alert)

                if len(results):
                    executed.append(
                        self._send_alert(alert, results),
                    )

        return executed

    def _check_alert(self, alert):
        """
        This method is responsible for selecting the appropriate
        third party to then query for the alert criteria.

        The helper method selected will do the actual heavy lifting.
        """
        match type(alert):
            case models.LookerAlert:
                return self._check_looker_alert(alert)

    def _check_looker_alert(self, alert):
        if self.looker is None:
            self.looker = Looker()

        return self.looker.query(alert.request_body())

    def _send_alert(self, alert, results):
        """
        Stub method.

        A proper implementation would actually send a notification,
        using a tool such as Sendgrid.

        For now this will just return the alert as it would be sent.
        """

        alert.update_last_checked()

        return {
            "to": alert.email,
            "subject": "New items found!",
            "body": results,
        }
