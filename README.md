# OZON SDK library for python 3.*
---

## Objects
    
    - Order ---+
                |
                +--+ 
    - Product --+
                |
                +--+ Product
                     ProductComission


### BaseProduct
    
    product_id: int (Default None)
    offer_id: str (Default None)
    stock_coming: int (Default None)
    stock_present: int (Default None)
    stock_reserved: int (Default None)
    price: float (Default None)
    old_price: float (Default None)
    premium_price: float (Default None)
    recommended_price: float (Default None)
    retail_price: float (Default None)
    vat: float (Default None)
    buybox_price: float (Default None)
    min_ozon_price: float (Default None)
    marketing_price: float (Default None)
    marketing_seller_priced: float (Default None)
    marketing_actions: str (Default None)
    volume_weight: float (Default None)
    commissions: List[ProductCommission] (Default [])                  

### ProductCommission

    percent: int (Default None)
    min_value: float (Default None)
    value: float (Default None)
    sale_schema: str (Default None)
    delivery_amount: float (Default None)
    return_amount: float (Default None)
    
---

## Methods

### get_base_products
(Method can return Product objects with stocks, prices and commissions.)

    
    from ozon_sdk.methods import get_base_products
    products = get_base_products(
        client_id: str = CLIENT_ID,
        api_key: str = API_KEY,
        products_in_chunk: int = 200,
        downloading_threads_max_count: int = 10,
        with_stocks: bool = True,
        with_prices: bool = True
    )
Function collects from Ozon API products with basic info like a prices, stocks, commissions.
    :param client_id: Client Id from own cabinet
    :param api_key: Api Key from own cabinet
    :param products_in_chunk: products count per page(Max=1000). How many items we can collect by 1 request.
    :param downloading_threads_max_count: How many threads we can use for collecting.
    (Ozon doesn't interested in much requests per minute)
    :param with_stocks: Returning products will be contains stocks data. Else None for stocks parameters.
    :param with_prices: Returning products will be contains prices and commissions data. Else None for prices parameters
    :return: List of Validated BaseProduct objects.<br>
    [[BaseProduct Object ](#Product)]
