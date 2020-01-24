university_web_site = 'https://service.handlowa.eu/Konto/LogowanieStudenta'


longitude = "user's longitude"
latitude = "user's latitude"


route_attributes = {"line-name" : "line-name", 
					     "travel-time" : "div.cn-travel-time",
					     "departure-time" : 'cn-first-stop', 
					     "arrival-time" : 'cn-end-route',
					     "time-before-departure" : "cn-departure-time"}

func_emojis = {"sun":b"\xE2\x98\x80".decode()+"Weather", 
                    "book":b'\xF0\x9F\x93\x99'.decode() + "Classes for today", 
                    "classes":b'\xF0\x9F\x8F\xAB'.decode() + "Upcoming classes", 
                    "plan" : b'\xF0\x9F\x9A\x8A'.decode() + "Plan you route",
                    "log_and_pass": b'\xF0\x9F\x94\x90'.decode() + "Login and Password"}

msg_emojis = {"confirmed_log": b'\xE2\x9C\x85'.decode() + "Login is confirmed",
                  "confirmed_pass": b'\xE2\x9C\x85'.decode() + "Password is confirmed",
                  "not_registered": b'\xF0\x9F\x9A\xA8'.decode() + "Welcome, probably you are not registered user, so you should enter the 'Secret word'...",
                  "warning": b'\xE2\x9A\xA0'.decode() + "Invalid secret code..."}

kbrd_emojis = {"login": b'\xF0\x9F\x94\x92'.decode() + "Enter LOGIN",
                  "password": b'\xF0\x9F\x94\x91'.decode() + "Enter PASSWORD",
                  "later": b'\xF0\x9F\x94\xB7'.decode() + "Go to functions"}


json_properties = {"classes" : [], 
                   "routes" : [], 
                   'last_update' : "", 
                   "missed_clss" : None}