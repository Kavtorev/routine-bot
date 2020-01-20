from settings import func_emojis

#text constants
main_keyboard_description = "{}: Current temperature in Wroclaw \
						   \n{}: Checks whether you have classes for today or not \
						   \n{}: Shows your upcoming classes for that week and partly for the next one \
						   \n{}: You can set up or change current password from University 'Dziekanat'".format(
							   			b'\xE2\x98\x80'.decode(), 
								   		b'\xF0\x9F\x93\x99'.decode(), 
										b'\xF0\x9F\x8F\xAB'.decode(), 
										b'\xF0\x9F\x94\x90'.decode())

authentication_description = b'\xF0\x9F\x94\x90'.decode() + "Set up or change your login or password:"

please_wait_notification = b'\xF0\x9F\x92\xBD'.decode() + "Please, wait."

not_registered_notification = "Welcome, probably you are not registered user, \
										so you should enter the 'Secret word'..."

no_classes = "You don't have classes for today..."

missed_all = "Congratulations, you are late for all classes!"

invalid_s_word = "Invalid secret code..."

you_are_welcome = "Welcome to the Family!"

authentication_trouble = "Wrong password or login..."

no_upcoming_classes = "You don't have any upcoming classes..."

bad_login = "Something wrong with your Login or Password. Please try to change them {} section".format(func_emojis['log_and_pass'])