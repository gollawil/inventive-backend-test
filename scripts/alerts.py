import os
import sys

cwd = os.getcwd()
sys.path.extend([cwd, f"{cwd}/src"])

from src.lib import AlertHandler  # noqa
from src.models import CustomerC1 # noqa


def main():
    alert_handler = AlertHandler()

    our_customers = CustomerC1.all()

    for c1 in our_customers:
        their_customers = c1.customers()

        for c2 in their_customers:
            alerts = c2.alerts()
            alert_handler.execute(alerts)


if __name__ == "__main__":
    main()
