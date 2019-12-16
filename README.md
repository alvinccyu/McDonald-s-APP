# McDaily API

> Please note that this app might stop working in the near future, as
> they have changed the hashing algorithm from simple MD5 to
> AES encryption + Base64 hashing using a differently formatted string.

API wrapper for interacting with the Taiwan McDaily app.

## Example

Obtain login token
```sh
python login.py
```

Login and interact with the McDaily app
```py
from McDaily__API import McDailyAccount

# Creat a object
account = McDailyAccount('Your token')

# Get lottery
account.lottery_get_item()

# Get the coupon list
coupon_list = account.coupon_get_list()
```

## Contributing

Thanks Still34
