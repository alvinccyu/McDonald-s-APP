from Mask import Mask


# User login form
username = input('Username : ')
password = input('Password : ')

# Login and get the imformation
account = Mask(username, password)
response = account.login()

# Print the results
print('')
print('Login status : ' + response['rm'])
print('Username     : ' + response['results']['member_info']['name']['last_name'] + response['results']['member_info']['name']['first_name'])
print('Token        : ' + response['results']['member_info']['access_token'])
