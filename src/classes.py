import os
import time
import json
import requests
import calendar
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from secrets import weather_api_key
from datetime import datetime, timedelta
from settings import route_attributes, longitude, latitude, university_web_site

class Base:
	path = os.getcwd()
	current_date_and_time = datetime.now()
	current_date_and_time_format = current_date_and_time.strftime("%Y-%m-%d")
	
	def __init__(self):
		pass

	@staticmethod
	def serialize(data, user_id):
		with open(f"users/{user_id}.json", 'w') as json_file:
			json.dump(data, json_file, indent = 4)

	@staticmethod
	def deserialize(user_id):
		with open(f"users/{user_id}.json", 'r') as json_file:
			data = json.load(json_file)
		return data

	@staticmethod	
	def update_json(user_id, keys, values):
		data = Base.deserialize(user_id)
		for key, value in zip(keys, values):
			data[key] = value
		Base.serialize(data, user_id)

	@staticmethod
	def get_json_value(user_id, key):
		data = Base.deserialize(user_id)
		return data[key]

	@staticmethod
	def init_driver():
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--incognito')
		options.add_argument('--headless')
		return webdriver.Chrome(f'{Base.path}/chromedriver/chromedriver', chrome_options = options)
	
	@staticmethod
	def def_the_limit(time):
		time_index = time.hour // 3
		if time.minute >= 30: time_index += 1
		return time_index

	@staticmethod	
	def time_difference(end_time, start_time, in_minutes = None):
		start_time = timedelta(hours = start_time.hour, minutes = start_time.minute)
		end_time = timedelta(hours = end_time.hour, minutes = end_time.minute)
		difference_in_minutes = ((end_time - start_time).seconds) // 60

		if in_minutes == True:
			return difference_in_minutes
		else:
			hours = difference_in_minutes // 60
			minutes = difference_in_minutes % 60
			hours_minutes = datetime.strptime(f"{hours}:{minutes}", "%H:%M")
			return hours_minutes

	@staticmethod
	def get_week_day(date):
		date = datetime.strptime(date, '%Y-%m-%d')
		day = date.weekday()
		return calendar.day_name[day]

	@staticmethod
	def close_browser(driver):
		driver.close()

class User:
	def __init__(self, login, password, user_id):
		self.login = login
		self.password = password
		self.id = user_id

class Transport:
	approximate_time_travel_min = 46
	tram_frequency_min = 12
	subtracted_time = datetime.strptime("1:10", "%H:%M") #approximate_time_travel_min + (tram_frequency * 2)

	def __init__(self):
		self.start_point = "Fryderyka Pautscha 5/7"
		self.end_point = "Aleksandra Ostrowskiego 22"
		self.todays_date_1 = Base.current_date_and_time.strftime("%d.%m.%y")
		self.transport_properties = ["Leave in", "Departure Time", "Arrival Time", "Travel Line"]
	
	def get_transport_time(self, time_class_starts, date, driver, user_id, missed_clss):
		try:
			data = Base.deserialize(user_id)
			if data['last_update'] == Base.current_date_and_time_format and data['routes'] != [] \
																and data['missed_clss'] == missed_clss:
				return data
		except Exception as e:
			print("Error:", e)

		time_class_starts = datetime.strptime(time_class_starts, "%H:%M")
		time_of_the_first_route = Base.time_difference(time_class_starts, Transport.subtracted_time).time().strftime("%H:%M")
		
		self.time = time_of_the_first_route
		self.date = date
		self.link = f"https://jakdojade.pl/wroclaw/trasa/z--Fryderyka-Pautscha-57--do--Aleksandra-Ostrowskiego-22?" + \
				     "fn=Fryderyka%20Pautscha%205~2F7&tn=Aleksandra%20Ostrowskiego%2022&tc=51.0943:16.97487&fc=51.101216:17.099739&" + \
					f"ft=LOCATION_TYPE_ADDRESS&tt=LOCATION_TYPE_ADDRESS&d={self.date}&h={self.time}&aro=1&t=1&rc=3&ri=1&r=0"
		driver.get(self.link)

		time.sleep(5)

		Transport.submit_button(driver)
		data = self.get_route_info(driver)

		Base.update_json(user_id, 
						['routes', "missed_clss", "last_update"], 
						[data['routes'], missed_clss, Base.current_date_and_time_format])
		
		Base.close_browser(driver)

		return data

	@staticmethod
	def submit_button(driver):
		confirm_button = driver.find_element_by_class_name('cmp-intro_acceptAll')
		confirm_button.click()

	def get_route_info(self, driver):
		time.sleep(5)
		transport_schedule = {"routes":[]}
		route_containers = driver.find_elements_by_css_selector("div.cn-route-header-content-container")

		for route_number, route in enumerate(route_containers):
			transport_schedule["routes"].append({})
			tmp_list = []

			time_before_departure_ = route.find_element_by_class_name(route_attributes['time-before-departure']).text.split()[1]
			tmp_list.append(time_before_departure_)
			
			departure_time_ = route.find_element_by_class_name(route_attributes['departure-time']).text.split()[0]
			tmp_list.append(departure_time_)
			
			arrival_time_ = route.find_element_by_class_name(route_attributes['arrival-time']).text
			tmp_list.append(arrival_time_)
			
			line_name_ = route.find_element_by_class_name(route_attributes['line-name']).text
			tmp_list.append(line_name_)
			
			travel_time_ = route.find_element_by_css_selector(route_attributes['travel-time']).text
			tmp_list.append(travel_time_)
			
			for prop, value in zip(self.transport_properties, tmp_list):
				transport_schedule["routes"][-1][prop] = value
		
		#dict 'routes':[{r1}{r2}{r3}]
		return transport_schedule

class Schedule:
	def __init__(self):
		self.todays_date = Base.current_date_and_time.strftime("%Y-%m-%d")
		self.classes_properties = ["subject", "start", "finish", "duration", "type_of_class"]
		self.missed_all = False
		self.missed_a_few = False
		
	def get_schedule_time(self, driver, login, password, user_id):
		try:
			data = Base.deserialize(user_id)
			if data['last_update'] == Base.current_date_and_time_format:
				return data
		except Exception as e:
			print("Error: ", e)

		driver.get(university_web_site)

		time.sleep(3)

		Schedule.open_schedule(driver, login, password)

		time.sleep(3)
		
		data = self.grab_data_from_schedule(driver)
		Base.update_json(user_id, ['classes', 'last_update'], 
						[data['classes'], Base.current_date_and_time_format])
		#json file 'classes'
		return data

	@staticmethod
	def open_schedule(driver, login, password):
		
		time.sleep(0.5)

		login_ = driver.find_element_by_name("login")
		password_ = driver.find_element_by_name("haslo")

		login_.send_keys(login)
		password_.send_keys(password)
		password_.send_keys(Keys.ENTER)
		time.sleep(2)
		
		try:
			driver.find_element_by_link_text("Plany zajęć").click()
		except:
			driver.find_element_by_link_text("Plans for classes").click()
		# driver.find_element_by_xpath('//*[@id="td_menu"]/ul[1]/li[5]/a').click()
		

	def grab_data_from_schedule(self, driver):
		schedule_parts = {"classes" :[]}
		row = 0
		while True:
			try:										
				date = driver.find_element_by_xpath(f'//*[@id="gridViewPlanyGrup_DXGroupRowExp{row}"]').text.split()[-2]
				schedule_parts['classes'].append({date: []})
				row += 1
				while True:
					class_info = {}
					try:
						class_ = driver.find_element_by_xpath(f'//*[@id="gridViewPlanyGrup_DXDataRow{row}"]')
						prop = class_.find_elements_by_class_name("dxgv")[1:6]
						prop.insert(0, prop.pop(3))
						for index, prop_ in enumerate(prop):
							class_info[self.classes_properties[index]] = prop_.text
							
						schedule_parts['classes'][-1][date].append(class_info)
						row += 1
					except Exception as e:
						break
			except Exception as e:
				break
		return schedule_parts

	def get_classes_for_tday(self, date, driver, login, password, user_id):
		data = self.get_schedule_time(driver, login, password, user_id)
		for i, date_ in enumerate(data['classes']):
			if date in date_:
				# print("\nDate was found and you probably gonna learn something today!\n")
				classes_for_today = data['classes'][i][date]
				#json [{cl1}{cl2}{cl3}]
				return classes_for_today
		else:
			return False

	def not_late_for(self, classes_for_today):
		time = Base.current_date_and_time.time()
		current_time = datetime.strptime(f"{time.hour}:{time.minute}", "%H:%M")
		classes_you_are_not_late_for = classes_for_today[:]
		self.classes_you_are_late_for = []
		
		for class_ in classes_for_today:			
			class_start_time = datetime.strptime(class_['start'], "%H:%M")
			difference_in_minutes = Base.time_difference(class_start_time, current_time, True)
		
			if current_time < class_start_time and \
					difference_in_minutes > Transport.approximate_time_travel_min + 5:
				#[{cl1}{cl2}]
				return classes_you_are_not_late_for
			else:
				self.missed_a_few = True
				self.classes_you_are_late_for.append(class_)
				classes_you_are_not_late_for.pop(0)

		self.missed_a_few = False
		return False

	def classes_to_visit(self, date, driver, login, password, user_id):
		classes_for_today = self.get_classes_for_tday(date, driver, login, password, user_id)
		if classes_for_today:
			classes_for_today = self.not_late_for(classes_for_today)
			if classes_for_today:
				#[{cl1}{cl2}]
				return classes_for_today
			else:
				self.missed_all = True
				return False
		else:
			return False			

	def get_list_of_all_classes(self, driver, login, password, user_id):
		data = self.get_schedule_time(driver, login, password, user_id)
		list_to_return = [class_ for class_ in data['classes']]
		#[{date:[{cl1 cl2}}, {date...}]
		print(list_to_return)
		return list_to_return
			
class Weather:
	def __init__(self):
		self.longitude = longitude
		self.latitude = latitude
		self.api_key = weather_api_key
		self.forecast_link = f'http://api.openweathermap.org/data/2.5/forecast?' + \
								f'lat={self.latitude}&lon={self.longitude}&units=metric&appid={self.api_key}'
		self.weather_link = f"http://api.openweathermap.org/data/2.5/weather?"+ \
								f"lat={self.latitude}&lon={self.longitude}&units=metric&appid={self.api_key}"

	def get_weather_forecast(self):
		request = requests.get(self.forecast_link)
		data = request.json()
		upper_limit = (24 - Base.current_date_and_time.hour) // 3 + 1
		data['list'] = data['list'][ :upper_limit]
		
		self.rain = Weather.get_rain(data['list'])
		self.the_coldest = Weather.get_the_coldest(data['list'])
		self.get_current_weather()

		Base.serialize(data, "weather_forecast")

	@staticmethod
	def get_rain(list_):
		for time_gap in list_:
			wDescription =  time_gap['weather'][-1]['description'].split()
			if 'rain' in wDescription:
				return ' '.join(wDescription)
		else:
			return "No rain for today!"

	@staticmethod
	def get_the_coldest(data):
		tmp = [time_gap['main']['temp_min'] for time_gap in data]
		return sorted(tmp)[0]

	def get_current_weather(self):
		request = requests.get(self.weather_link)
		data = request.json()
		
		self.current_temp = data['main']['temp']
		self.description = data['weather'][-1]['description'].title()

		Base.serialize(data, "current_weather")
		

	













