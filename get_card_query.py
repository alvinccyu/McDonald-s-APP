from Mask import Mask


# Login and get the token
account = Mask('username', 'password', 'card_no')
account.login()

# Get the card imformation
response = account.get_card_query()

# Print the results
print('')
print('Money  : ' + response['bonusList'][2]['bonusVO']['qunatity'])
print('Points : ' + response['bonusList'][1]['bonusVO']['qunatity'])
