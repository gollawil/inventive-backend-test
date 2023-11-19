from dotenv import load_dotenv
import looker_sdk

load_dotenv()

# For this to work you must either have set environment variables
# or created a looker.ini as described below in "Configuring the SDK"
sdk = looker_sdk.init40()  # or init31() for the older v3.1 API
my_user = sdk.me()

results = sdk.run_inline_query(
    result_format="json",
    body={
        "model": "thelook_partner",
        "view": "order_items",
        "fields": [
            "order_items.sale_price",
            "products.category",
            "products.item_name",
        ],
        "filters": {
            "order_items.sale_price": ">200",
            "products.category": "Pants"
        },
    },
)
