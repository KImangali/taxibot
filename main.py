import telebot #telegramAPIbot
from telebot import types #KeyboardButton

import random #random number

import datetime #date and time
from datetime import datetime, timedelta
from datetime import date
import csv #read and write to csv file

#for graphs
import matplotlib
matplotlib.use('Agg')
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

import calendar #to get month name EX: December, January

import pytz #timezone hosting isn't in KZ
country_time_zone = pytz.timezone('Asia/Almaty')

current_datetime = datetime.now(country_time_zone)#to get current_datetime of KZ

#BOT DATA
token = '1416332736:AAFS-quEAN1WDRzBcCWhJGi1wAP4q4Efl5c'#'1480915875:AAHueekmP3g0szKc7goexrIZoOi1hQH8E3A'
bot = telebot.TeleBot(token)
otyrartaxi_id = "@otyrartaxi"

#Necessary for USERs
fullname = ''
phone = 0
user_dict = {}
driver_dict = {}
class User:
    def __init__(self, A):
        self.A = A
        keys = ['B', 'date', 'month', 'price' 'full_date', 'hour', 'comment']
        for key in keys:
            self.key = None
class Driver:
	def __init__(self, A):
		self.A = A
		keys = ['B', 'date', 'month', 'price', 'full_date', 'hour', 'comment']
		for key in keys:
			self.key = None

#---------------START-------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
	#deleting overdue requests
	requests = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
	ind = 0
	while(ind < len(requests)):
		day = requests['day'][ind]
		month = requests['month'][ind]
		year = requests['year'][ind]
		empty = requests['time'][ind]
		idp = empty.index(':')
		hour = empty[:idp]
		minute = empty[idp+1:]
		userchatid_for_rem = requests['chat_id'][ind]
		full_time = requests['time'][ind]
		user_message_id = requests['message_id'][ind]
		user_from =  requests['from'][ind]
		user_to =  requests['to'][ind]
		user_comment =  requests['comment'][ind]
		user_status =  requests['status'][ind]
		if(pd.isnull(user_status)):
			isTRUE = ((int(month)<int(current_datetime.month)) or (int(day)<int(current_datetime.day) and int(month)==int(current_datetime.month)) or (int(day)==int(current_datetime.day) and int(month)==int(current_datetime.month) and int(hour)<int(current_datetime.hour)) or (int(day)==int(current_datetime.day) and int(month)==int(current_datetime.month) and int(hour)==int(current_datetime.hour) and int(minute)<int(current_datetime.minute)))
			if(isTRUE):
				bot.delete_message(otyrartaxi_id, int(user_message_id))
				user_status = 'выполнен'
				requests = requests.drop(index=ind)
				request = pd.DataFrame({"chat_id":[userchatid_for_rem],
										"message_id":[user_message_id],
										"from":[user_from],
										"to":[user_to],
										"day":[day],
										"month":[month],
										"year":[year],
										"time":[full_time],
										"comment":[user_comment],
										"status":[user_status]})
				requests = requests.append(request, ignore_index=True)
				#writing to scv file
				requests.to_csv(r'users_requests.csv', index = False, header=True, encoding='cp1251')
				#deleting from resending_req_driver.csv
				rtd = pd.read_csv('resending_req_driver.csv', sep=',', encoding='cp1251')
				rtds = rtd[rtd['group_message_id']==user_message_id]
				if(rtds.empty==False):
					driver_id = rtds['driver_id'].values
					driver_id = int(driver_id[0])
					message_id = rtds['driver_message_id'].values
					message_id = int(message_id[0])
					bot.delete_message(driver_id, message_id)
					indices = 0
					rtd = rtd[rtd['group_message_id']!=int(user_message_id)]
					rtd.to_csv(r'resending_req_driver.csv', index = False, header=True, encoding='cp1251')
				#deleting from resending_req_user.csv
				rtu = pd.read_csv('resending_req_user.csv', sep=',', encoding='cp1251')
				rtus = rtu[rtu['group_message_id']==user_message_id]
				if(rtus.empty==False):
					user_id = rtus['user_id'].values
					user_id = int(user_id[0])
					message_id = rtus['to_user_message_id'].values
					message_id = int(message_id[0])
					bot.delete_message(user_id, message_id)
					indices = 0
					rtu = rtu[rtu['group_message_id']!=int(user_message_id)]
					rtu.to_csv(r'resending_req_user.csv', index = False, header=True, encoding='cp1251')

				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
				itembtn1 = types.KeyboardButton('Пpoдoлжить')
				markup.add(itembtn1)
				bot.send_message(int(userchatid_for_rem), "Заказывайте я вам только рад :)", reply_markup = markup)
			else:
				ind+=1
		else:
			ind+=1

	#LOOK FOR user in users.csv
	users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
	user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
	exists = False
	isTaxi = False
	for index, row in users.iterrows():
		if row['chat_id']==user_chat_id:
			if row['taxi'] == 'y':
				isTaxi = True
			exists = True

	if(exists==True and isTaxi==False):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
		itembtn2 = types.KeyboardButton('/Настройки⚙️')
		markup.add(itembtn1, itembtn2)
		msg = bot.send_message(message.chat.id, "Можете совершать услуги.", reply_markup = markup)
	elif(exists==True and isTaxi==True):
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('Добавить заявку➕')
		itembtn2 = types.KeyboardButton('Статистика📈')
		itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
		markup.add(itembtn1, itembtn2, itembtn3)
		msg = bot.send_message(message.chat.id, "Вы в режиме водиетеля!\nВ Статистика📈 можете посмотреть статистику запросов от клиентов", reply_markup = markup)
		bot.register_next_step_handler(msg, chosing_diver)
	else:
		sti = open('static/welcome.webp', 'rb')
		bot.send_sticker(message.chat.id, sti)
		sti.close()

		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Регистрация')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Салем, {0.first_name}!\n Я - <b>{1.first_name}</b>, такси бот. Чтобы пользоваться моими услугами вы должны зарегистрироваться как пользователь.".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup = markup)
#---------------end-START------------------------------------------------------------------------------------------------------------------

#---------------REGISTRATION---------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['Регистрация'])
def registration(message):
	try:
		markup = types.ReplyKeyboardRemove(selective=False)
		msg = bot.send_message(message.chat.id, 'Введите ваше Имя', reply_markup = markup)
		bot.register_next_step_handler(msg, process_name)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Регистрация process_name!')

def process_name(message):
	try:
		global fullname
		fullname = message.text
		msg = bot.send_message(message.chat.id, 'Номер:\nПример: 87771234656')
		bot.register_next_step_handler(msg, process_phone)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Регистрация process_name!')

def process_phone(message):
	try:
		if len(message.text) != 11:
			msg = bot.send_message(message.chat.id, 'Длина номера не равен 11. Введите заново.')
			bot.register_next_step_handler(msg, process_phone)
		elif message.text[0] != '8':
			msg = bot.send_message(message.chat.id, 'Номер должен начинаться с 8. Введите заново.')
			bot.register_next_step_handler(msg, process_phone)
		elif message.text[1]!='7':
			msg = bot.send_message(message.chat.id, 'Для операторов РК вторая цифра номера 7. Введите заново.')
			bot.register_next_step_handler(msg, process_phone)
		else:
			global fullname
			try:
				#reading from csv file
				join_date = str(current_datetime.day) +'.'+ str(current_datetime.month) +'.'+ str(current_datetime.year)
				users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
				user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
				new_user = [{"chat_id":user_chat_id,
							"fullname":fullname,
							"phone":int(message.text),
							"join_date":join_date, 
							"taxi":'n'}]
				exists = False
				for index, row in users.iterrows():
					if row['chat_id']==user_chat_id:
						exists = True

				if(exists==False):
					users = users.append(new_user, ignore_index = True)
					#writing to scv file
					users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')

				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
				itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
				itembtn2 = types.KeyboardButton('/Настройки⚙️')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, "Можете совершать услуги.", reply_markup = markup)
			except Exception as f:
				msg = bot.send_message(message.chat.id, 'Если я не ошибаюсь номер телефона состоит только из цифр.🤔\nВведите заново.')
				bot.register_next_step_handler(msg, process_phone)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Регистрация process_phone!')
#---------------end-REGISTRATION-------------------------------------------------------------------------------------------------------

#---------------SETTINGS---------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['Настройки⚙️'])
def settings(message):
	try:
		sti = open('static/setting.jpg', 'rb')
		bot.send_photo(message.chat.id, sti)
		sti.close()
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		itembtn1 = types.KeyboardButton('Изменить имя')
		itembtn2 = types.KeyboardButton('Изменить номер')
		itembtn3 = types.KeyboardButton('Стать Водителем🚕')
		itembtn4 = types.KeyboardButton('🔙Назад')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
		msg = bot.send_message(message.chat.id, "Если выбрать 'Стать Водителем🚕', не так уж сложно будет стать крутым таксистом🚖", reply_markup = markup)
		bot.register_next_step_handler(msg, choosing_setting)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Настройки settings!')

def choosing_setting(message):
	try:
		if(message.text=='Изменить имя'):
			markup = types.ReplyKeyboardRemove(selective=False)
			msg = bot.send_message(message.chat.id, "Введите имя:", reply_markup = markup)
			bot.register_next_step_handler(msg, changing_name)
		elif(message.text=='Изменить номер'):
			markup = types.ReplyKeyboardRemove(selective=False)
			msg = bot.send_message(message.chat.id, "Введите номер:", reply_markup = markup)
			bot.register_next_step_handler(msg, changing_phone)
		elif(message.text=='Стать Водителем🚕'):
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Подтвердить')
			itembtn2 = types.KeyboardButton('/Настройки⚙️')
			markup.add(itembtn1, itembtn2)
			msg = bot.send_message(message.chat.id, "Приоритеты стать водителем\n 1. Я дублирую сообщения вам в личку\n 2. Вам будут приходить отсортированные сообщения с города А и до города B выбранные вами.\n  Когда вы станете водителем вы не можете добавлять заказы как клиент, чтобы добавить заказ как клиент, вам нужно перейти в режим Клиента👤.\n Или можете вступить в группу otyrartaxi и брать заказы там.\n  Если хотите стать Водителем🚕 Подтвердите✅ ваш выбор или перейдите назад в Настройки⚙️", reply_markup = markup)
		elif(message.text=='🔙Назад'):
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
			itembtn2 = types.KeyboardButton('/Настройки⚙️')
			markup.add(itembtn1, itembtn2)
			msg = bot.send_message(message.chat.id, "Совершайте услуги, я вам только рад🙃", reply_markup = markup)
		else:
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Изменить имя')
			itembtn2 = types.KeyboardButton('Изменить номер')
			itembtn3 = types.KeyboardButton('Стать Водителем🚕')
			itembtn4 = types.KeyboardButton('🔙Назад')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Такой операции не существует!', reply_markup=markup)
			bot.register_next_step_handler(msg, choosing_setting)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Настройки choosing_setting!')

def changing_name(message):
	try:
		#reading from csv file
		user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		user_new_fullname = message.text
		user_old_fullname = ''
		tel_phone = 0
		join_date = ''
		taxi = ''
		users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
		
		for ind in users.index:
			if users['chat_id'][ind]==user_chat_id:
				user_old_fullname = users['fullname'][ind]
				tel_phone = users['phone'][ind]
				join_date = users['join_date'][ind]
				taxi = users['taxi'][ind]

		users = users[users['chat_id'] != user_chat_id]
		user = pd.DataFrame({"chat_id":[user_chat_id], 
							"fullname":[user_new_fullname],
							"join_date":[join_date],
							"phone":[tel_phone],
							"taxi":[taxi]})
		users = users.append(user, ignore_index=True)
		#writing to scv file
		users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
		itembtn1 = types.KeyboardButton('Изменить имя')
		itembtn2 = types.KeyboardButton('Изменить номер')
		itembtn3 = types.KeyboardButton('Стать Водителем🚕')
		itembtn4 = types.KeyboardButton('🔙Назад')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
		msg = bot.send_message(message.chat.id, 'Имя успешно изменен!', reply_markup=markup)
		bot.register_next_step_handler(msg, choosing_setting)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Настройки changing_name!')
def changing_phone(message):
	try:
		if len(message.text) != 11:
			msg = bot.send_message(message.chat.id, 'Длина номера не равен 11. Введите заново.')
			bot.register_next_step_handler(msg, changing_phone)
		elif message.text[0] != '8':
			msg = bot.send_message(message.chat.id, 'Номер должен начинаться с 8. Введите заново.')
			bot.register_next_step_handler(msg, changing_phone)
		elif message.text[1]!='7':
			msg = bot.send_message(message.chat.id, 'Для операторов РК вторая цифра номера 7. Введите заново.')
			bot.register_next_step_handler(msg, changing_phone)
		else:
			try:
				#reading from csv file
				user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
				user_new_phone = int(message.text)
				full_name = ''
				taxi = ''
				users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
				
				for ind in users.index:
					if users['chat_id'][ind]==user_chat_id:
						full_name = users['fullname'][ind]
						join_date = users['join_date'][ind]
						taxi = users['taxi'][ind]

				users = users[users['chat_id'] != user_chat_id]
				user = pd.DataFrame({"chat_id":[user_chat_id], 
									"fullname":[full_name],
									"phone":[user_new_phone],
									"join_date":[join_date],
									"taxi":[taxi]})
				users = users.append(user, ignore_index=True)
				#writing to scv file
				users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')
				markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Изменить имя')
				itembtn2 = types.KeyboardButton('Изменить номер')
				itembtn3 = types.KeyboardButton('Стать Водителем🚕')
				itembtn4 = types.KeyboardButton('🔙Назад')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Номер успешно изменен!', reply_markup=markup)
				bot.register_next_step_handler(msg, choosing_setting)
			except Exception as f:
				msg = bot.send_message(message.chat.id, 'Если я не ошибаюсь номер телефона состоит только из цифр.🤔\nВведите заново.')
				bot.register_next_step_handler(msg, changing_phone)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Настройки changing_phone!')

#---------------end-SETTINGS--------------------------------------------------------------------------------------------------------------

#---------------NEW_REQUEST---------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['Новый_Заказ🟢'])
def process_from(message):
	try:
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
		itembtn1 = types.KeyboardButton('Шаульдер')
		itembtn2 = types.KeyboardButton('Шымкент')
		itembtn3 = types.KeyboardButton('Туркестан')
		itembtn4 = types.KeyboardButton('Алматы')
		itembtn5 = types.KeyboardButton('Нур-Султан')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

		msg = bot.send_message(message.chat.id, 'Откуда(точка A)?', reply_markup=markup)
		bot.register_next_step_handler(msg, process_to)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_from!')

def process_to(message):
	try:
		if message.text=='Шаульдер' or message.text=='Шымкент' or message.text=='Туркестан' or message.text=='Алматы' or message.text=='Нур-Султан':
			#new_data
			user_dict[message.chat.id] = User(message.text)
			
			if message.text == "Шаульдер":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шымкент')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif message.text == "Шымкент":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif message.text == "Туркестан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif message.text == "Алматы":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif message.text == "Нур-Султан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Алматы')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			itembtn5 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
			msg = bot.send_message(message.chat.id, 'Выберите только из списка!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_to!')

def process_date(message):
	try:
		if message.text=='Шаульдер' or message.text=='Шымкент' or message.text=='Туркестан' or message.text=='Алматы' or message.text=='Нур-Султан':
			user = user_dict[message.chat.id]
			user.B = message.text
			#printing date of weeks
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
			weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
			# for wd in weekdays:
			month = str((current_datetime).strftime("%B"))
			if month == 'January':
				month = 'Январь'
			elif month == 'February':
				month = 'Февраль'
			elif month == 'March':
				month = 'Март'
			elif month == 'April':
				month = 'Апрель'
			elif month == 'May':
				month = 'Май'
			elif month == 'June':
				month = 'Июнь'
			elif month == 'July':
				month = 'Июль'
			elif month == 'August':
				month = 'Август'
			elif month == 'September':
				month = 'Сентябрь'
			elif month == 'October':
				month = 'Октябрь'
			elif month == 'November':
				month = 'Ноябрь'
			elif month == 'December':
				month = 'Декабрь'
			itembtn = types.KeyboardButton(month)
			markup.add(itembtn)
			itembtn1 = types.KeyboardButton('Пн')
			itembtn2 = types.KeyboardButton('Вт')
			itembtn3 = types.KeyboardButton('Ср')
			itembtn4 = types.KeyboardButton('Чт')
			itembtn5 = types.KeyboardButton('Пт')
			itembtn6 = types.KeyboardButton('Сб')
			itembtn7 = types.KeyboardButton('Вс')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
			
			today_wd = str(current_datetime.strftime("%A"))#week day понедельник
			today_date = str((current_datetime).day)#todays date 23
			isequal = False

			#printing days
			weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
			btn_counter = 1
			i = 0
			size_of_btn_row = 0
			days10 = 0
			while i < 21:
				if(size_of_btn_row<7):
					if(isequal==False and weekdays[i]!=today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						size_of_btn_row+=1
					elif(isequal==False and weekdays[i]==today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(today_date)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(today_date)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(today_date)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(today_date)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(today_date)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(today_date)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(today_date)
						isequal=True
						i+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10<8):
						itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(itembtnday)
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10==8):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
					else:
						print("Not correct ads")
				elif(size_of_btn_row==7):
					markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
					size_of_btn_row = 0
			msg = bot.send_message(message.chat.id, 'День:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time)
		else:
			user = user_dict[message.chat.id]
			if user.A == "Шаульдер":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шымкент')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif user.A == "Шымкент":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif user.A == "Туркестан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif user.A == "Алматы":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif user.A == "Нур-Султан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Алматы')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_date!')
		
def process_time(message):
	try:
		if(int(message.text)<0 or int(message.text)>31):
			f = 0/0
		user = user_dict[message.chat.id]
		user.date = int(message.text)
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
		if int(user.date)==int(current_datetime.day):
			current_hour = int(current_datetime.hour)
			current_minute = int(current_datetime.minute)
			if(current_minute >= 30):
				current_minute = '00'
				current_hour+=1
			else:
				current_minute = '30'
			butnequaltf = False
			while current_hour!=24:
				print_time1 = ''
				print_time2 = ''
				if(current_hour<10):
					print_time1 = '0'+str(current_hour)+':'+current_minute
					if current_minute=='30':
						current_hour+=1
						current_minute = '00'
					elif current_minute=='00':
						current_minute = '30'
					if(current_hour<10):
						print_time2 = '0'+str(current_hour)+':'+current_minute
						if current_minute=='30':
							current_hour+=1
							current_minute = '00'
						elif current_minute=='00':
							current_minute = '30'
				elif(current_hour>=10):
					print_time1 = str(current_hour)+':'+current_minute
					if current_minute=='30':
						current_hour+=1
						current_minute = '00'
					elif current_minute=='00':
						current_minute = '30'
					if(current_hour>=10 and current_hour!=24):
						print_time2 = str(current_hour)+':'+current_minute
						if current_minute=='30':
							current_hour+=1
							current_minute = '00'
						elif current_minute=='00':
							current_minute = '30'
					else:
						butnequaltf = True
				if(butnequaltf==False):
					itembtn1 = types.KeyboardButton(print_time1)
					itembtn2 = types.KeyboardButton(print_time2)
					markup.add(itembtn1, itembtn2)
				elif(butnequaltf==True):
					itembtn1 = types.KeyboardButton(print_time1)
					markup.add(itembtn1)
		else:
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
		msg = bot.send_message(message.chat.id, 'Время:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_comment)
	except Exception as e:
		user = user_dict[message.chat.id]
		#printing date of weeks
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
		weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
		# for wd in weekdays:
		month = str((current_datetime).strftime("%B"))
		if month == 'January':
			month = 'Январь'
		elif month == 'February':
			month = 'Февраль'
		elif month == 'March':
			month = 'Март'
		elif month == 'April':
			month = 'Апрель'
		elif month == 'May':
			month = 'Май'
		elif month == 'June':
			month = 'Июнь'
		elif month == 'July':
			month = 'Июль'
		elif month == 'August':
			month = 'Август'
		elif month == 'September':
			month = 'Сентябрь'
		elif month == 'October':
			month = 'Октябрь'
		elif month == 'November':
			month = 'Ноябрь'
		elif month == 'December':
			month = 'Декабрь'
		itembtn = types.KeyboardButton(month)
		markup.add(itembtn)
		itembtn1 = types.KeyboardButton('Пн')
		itembtn2 = types.KeyboardButton('Вт')
		itembtn3 = types.KeyboardButton('Ср')
		itembtn4 = types.KeyboardButton('Чт')
		itembtn5 = types.KeyboardButton('Пт')
		itembtn6 = types.KeyboardButton('Сб')
		itembtn7 = types.KeyboardButton('Вс')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
		
		today_wd = str(current_datetime.strftime("%A"))#week day ex: Monday
		today_date = str((current_datetime).day)#todays date ex: 23
		isequal = False

		#printing days
		weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		btn_counter = 1
		i = 0
		size_of_btn_row = 0
		days10 = 0
		while i < 21:
			if(size_of_btn_row<7):
				if(isequal==False and weekdays[i]!=today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					size_of_btn_row+=1
				elif(isequal==False and weekdays[i]==today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(today_date)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(today_date)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(today_date)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(today_date)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(today_date)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(today_date)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(today_date)
					isequal=True
					i+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10<8):
					itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(itembtnday)
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10==8):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
				else:
					print("Not correct ads")
			elif(size_of_btn_row==7):
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
				size_of_btn_row = 0
		msg = bot.send_message(message.chat.id, 'Выберите только те дни которые есть в календаре!', reply_markup=markup)
		bot.register_next_step_handler(msg, process_time)

def process_comment(message):
	try:
		time = message.text
		if(time[2]!=':'):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_comment)
		elif(int(time[0:2])>24 or int(time[0:2])<0 or int(time[3:])<0 or int(time[3:])>60):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_comment)
		else:
			user = user_dict[message.chat.id]
			user.hour = message.text
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('-')
			markup.add(itembtn1)
			msg = bot.send_message(message.chat.id, 'Коментарий:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_price)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_message!')
def process_price(message):
	try:
		user = user_dict[message.chat.id]
		user.comment = message.text
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
		itembtn1 = types.KeyboardButton('1000')
		itembtn2 = types.KeyboardButton('1500')
		itembtn3 = types.KeyboardButton('2000')
		markup.add(itembtn1, itembtn2, itembtn3)
		msg = bot.send_message(message.chat.id, 'Выберите Стоимость или введите: ', reply_markup=markup)
		bot.register_next_step_handler(msg, process_prefinishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_price!')

#---------------finishing of NEW_REQUEST---------------
def process_prefinishing(message):
	try:
		try:
			user = user_dict[message.chat.id]
			user.price = int(message.text)
			if(user.price<0):
				msg = bot.send_message(message.chat.id, 'Цена не может быть отрицательным! Введите или выберите заново.', reply_markup=markup)
				bot.register_next_step_handler(msg, process_prefinishing)
			else:
				#getting fullname and phone from users.csv file
				global fullname
				global phone
				users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
				fn = users[users['chat_id']==message.chat.id]['fullname'].values
				fullname = fn[0]
				ph = users[users['chat_id']==message.chat.id]['phone'].values
				phone = ph[0]
				if(user.date<int((current_datetime).day)):
					user.month = str(int(current_datetime.month)+1)
					month = calendar.month_name[(int(current_datetime.month)+1)]
					if month == 'January':
						month = 'янв.'
					elif month == 'February':
						month = 'фев.'
					elif month == 'March':
						month = 'мар.'
					elif month == 'April':
						month = 'апр.'
					elif month == 'May':
						month = 'май'
					elif month == 'June':
						month = 'июн.'
					elif month == 'July':
						month = 'июл.'
					elif month == 'August':
						month = 'авг.'
					elif month == 'September':
						month = 'сен.'
					elif month == 'October':
						month = 'окт.'
					elif month == 'November':
						month = 'ноя.'
					elif month == 'December':
						month = 'дек.'
					user.full_date = str(user.date)+' '+str(month)
				elif(user.date>int((current_datetime).day)):
					user.month = str(current_datetime.month)
					month = calendar.month_name[int(current_datetime.month)]
					if month == 'January':
						month = 'янв.'
					elif month == 'February':
						month = 'фев.'
					elif month == 'March':
						month = 'мар.'
					elif month == 'April':
						month = 'апр.'
					elif month == 'May':
						month = 'май'
					elif month == 'June':
						month = 'июн.'
					elif month == 'July':
						month = 'июл.'
					elif month == 'August':
						month = 'авг.'
					elif month == 'September':
						month = 'сен.'
					elif month == 'October':
						month = 'окт.'
					elif month == 'November':
						month = 'ноя.'
					elif month == 'December':
						month = 'дек.'
					user.full_date = str(user.date)+' '+str(month)
				elif(user.date==int(current_datetime.day)):
					user.month = str(current_datetime.month)
					user.full_date = 'Сегодня'

				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Заказать✅')
				itembtn2 = types.KeyboardButton('Изменить✏️')
				itembtn3 = types.KeyboardButton('Отмена🚫')
				markup.add(itembtn1, itembtn2, itembtn3)
				last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
				msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
				bot.register_next_step_handler(msg, process_finishing)
		except Exception as e:
			msg = bot.send_message(message.chat.id, 'Введите только цифры')
			bot.register_next_step_handler(msg, process_prefinishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_prefinishing!')

def process_finishing(message):
	try:
		global fullname
		global phone
		user = user_dict[message.chat.id]
		user_chat_id = message.chat.id
		user_from = user.A
		user_to = user.B
		user_price = str(user.price)
		user_time = user.hour
		user_comment = user.comment
		user_date = user.date
		user_month = user.month
		user_year = str(current_datetime.year)
		user_status = ''
		user_message_id = 0
		if message.text=='Заказать✅':

			last_text = '<b>КЛИЕНТ, '+str(user.price)+'</b>\n👤:  <a href="tg://user?id={0.id}">' + fullname + '</a>, ' + str(phone) + '\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
			msg = bot.send_message(otyrartaxi_id, last_text.format(message.from_user, bot.get_me()), parse_mode='html')
			user_message_id = int(msg.id)

			requests_df = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
			request = pd.DataFrame({"chat_id":[user_chat_id],
									"message_id":[user_message_id],
									"from":[user_from],
									"to":[user_to],
									"price":[user_price],
									"day":[user_date],
									"month":[user_month],
									"year":[user_year],
									"time":[user_time],
									"comment":[user_comment],
									"status":[user_status]})
			requests_df = requests_df.append(request, ignore_index=True)
			#writing to scv file
			requests_df.to_csv(r'users_requests.csv', index = False, header=True, encoding='cp1251')
				#~~~sending requests from me to other drivers --AND-- from other drivers to me
			is_requests = False #to check is there only online requests
			resending_to_drivers = pd.read_csv('resending_req_driver.csv', sep=',', encoding='cp1251')
			resending_to_me_user = pd.read_csv('resending_req_user.csv', sep=',', encoding='cp1251')
				#~~~to check online requests
			drivers_requests = pd.read_csv('drivers_requests.csv', sep=',', encoding='cp1251')
				#~~~to get is user taxi or not and get phone
			users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
			for ind in users.index:
				if (users['taxi'][ind]=='y'):
					driver_reqs = drivers_requests[drivers_requests['chat_id']==users['chat_id'][ind]]
					driver_reqs = driver_reqs[pd.isnull(driver_reqs['status'])]
					driver_reqs = driver_reqs[driver_reqs['from']==user.A]
					driver_reqs = driver_reqs[driver_reqs['to']==user.B]
					driver_reqs = driver_reqs[driver_reqs['day']==int(user_date)]
					driver_reqs = driver_reqs[driver_reqs['month']==int(user_month)]
					if(driver_reqs.empty==False):
						driver_id = int(users['chat_id'][ind])
						to_driver_message_id = driver_reqs['message_id'].values
						to_driver_message_id = int(to_driver_message_id[0])
						d_fullname = users['fullname'][ind]
						d_phone = users['phone'][ind]
						d_A = driver_reqs['from'].values
						d_A = d_A[0]
						d_B = driver_reqs['to'].values
						d_B = d_B[0]
						d_price = driver_reqs['price'].values
						d_price = d_price[0]
						d_date = driver_reqs['day'].values
						d_date = d_date[0]
						d_month = driver_reqs['month'].values
						d_month = d_month[0]
						d_time = driver_reqs['time'].values
						d_time = d_time[0]
						d_comment = driver_reqs['comment'].values
						d_comment = d_comment[0]
						#------------------------------------------
						#send my request to other online drivers 
						msg = bot.send_message(int(driver_id), last_text.format(message.from_user, bot.get_me()), parse_mode='html')
						res_to_driver = pd.DataFrame({"chat_id":[user_chat_id],#from me
													"group_message_id":[user_message_id],
													"driver_id":[driver_id],#to driver
													"driver_message_id":[msg.id]})
						resending_to_drivers = resending_to_drivers.append(res_to_driver, ignore_index=True)
						resending_to_drivers.to_csv(r'resending_req_driver.csv', index = False, header=True, encoding='cp1251')
						#------------------------------------------
						#send other driver online requests to me, text to me user
						text_to_user = '<b>TAXI, '+str(d_price)+'</b>\n👤: <a href="tg://user?id='+str(driver_id)+'">' + d_fullname + '</a>, ' + str(d_phone) + '\n A:  <i><b>' + d_A + '</b></i>\n B:  <i><b>' + d_B + '</b></i>\n 📅: <i><b>' + str(d_date)+'.'+str(d_month) + '</b></i> в <i><b>' + d_time + '</b>\n  ' + d_comment + '</i>'
						
						msg = bot.send_message(message.chat.id, text_to_user, parse_mode='html')
						res_to_me = pd.DataFrame({"chat_id":[driver_id],#from drivers
													"group_message_id":[to_driver_message_id],
													"user_id":[user_chat_id],#to me
													"to_user_message_id":[msg.id]})
						resending_to_me_user = resending_to_me_user.append(res_to_me, ignore_index=True)
						resending_to_me_user.to_csv(r'resending_req_user.csv', index = False, header=True, encoding='cp1251')
						is_requests = True
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Отменить заказ🚫')
			markup.add(itembtn1)	
			if(is_requests==False):
				msg = bot.send_message(message.chat.id, '🎟️ Ваш заказ добавлен!\n🧾 Код остановки заказа: ' + str(user_message_id), reply_markup=markup)
				msg = bot.send_message(message.chat.id, 'Пока нету таксистов по вашему маршруту в данный день. Если появятся, я вам сообщу. Будьте онлайн!.')
				bot.register_next_step_handler(msg, process_canceling)
			else:
				msg = bot.send_message(message.chat.id, '🎟️ Ваш заказ добавлен! Вот список таксиситов по вашему маршруту в данный день. Если появятся еще я вам сообщу. Будьте онлайн!\n🧾 Код остановки заказа: ' + str(user_message_id), reply_markup=markup)
				bot.register_next_step_handler(msg, process_canceling)
		elif message.text=='Изменить✏️':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Имя')
			itembtn2 = types.KeyboardButton('Номер')
			itembtn3 = types.KeyboardButton('A')
			itembtn4 = types.KeyboardButton('B')
			itembtn5 = types.KeyboardButton('День')
			itembtn6 = types.KeyboardButton('Время')
			itembtn7 = types.KeyboardButton('Коментарий')
			itembtn8 = types.KeyboardButton('Стоимость')
			itembtn9 = types.KeyboardButton('⬅️НАЗАД')
			
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)
			
			msg = bot.send_message(message.chat.id, 'Что хотите изменять?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_editing)
		else:
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
			itembtn2 = types.KeyboardButton('/Настройки⚙️')
			markup.add(itembtn1, itembtn2)
			
			msg = bot.send_message(message.chat.id, "{0.first_name} чтобы заказать нажмите на кнопку ниже".format(message.from_user, bot.get_me()), reply_markup = markup)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_finishing!')
#---------------END-NEW_REQUEST---------------------------------------------------------------------------------------------------------------

#---------------EDITING-----------------------------------------------------------------------------------------------------------------------
def process_editing(message):
	try:
		#удалить старую клавиатуру
		markup = types.ReplyKeyboardRemove(selective=False)
		if message.text=='Имя':
			msg = bot.send_message(message.chat.id, 'Введите имя: ')
			bot.register_next_step_handler(msg, process_name_edit)
		elif message.text=='Номер':
			msg = bot.send_message(message.chat.id, 'Введите номер \n Пример: 87771234656')
			bot.register_next_step_handler(msg, process_phone_edit)
		elif message.text=='A':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			itembtn5 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

			msg = bot.send_message(message.chat.id, 'Выберите точку А!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_from_edit)
		elif message.text=='B':
			user = user_dict[message.chat.id]
			if user.A == "Шаульдер":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шымкент')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_to_edit)
			elif user.A == "Шымкент":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_to_edit)
			elif user.A == "Туркестан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_to_edit)
			elif user.A == "Алматы":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_to_edit)
			elif user.A == "Нур-Султан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Алматы')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				bot.register_next_step_handler(msg, process_to_edit)
		elif message.text=='День':
			user = user_dict[message.chat.id]
			#printing date of weeks
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
			weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
			# for wd in weekdays:
			month = str((current_datetime).strftime("%B"))
			if month == 'January':
				month = 'Январь'
			elif month == 'February':
				month = 'Февраль'
			elif month == 'March':
				month = 'Март'
			elif month == 'April':
				month = 'Апрель'
			elif month == 'May':
				month = 'Май'
			elif month == 'June':
				month = 'Июнь'
			elif month == 'July':
				month = 'Июль'
			elif month == 'August':
				month = 'Август'
			elif month == 'September':
				month = 'Сентябрь'
			elif month == 'October':
				month = 'Октябрь'
			elif month == 'November':
				month = 'Ноябрь'
			elif month == 'December':
				month = 'Декабрь'
			itembtn = types.KeyboardButton(month)
			markup.add(itembtn)
			itembtn1 = types.KeyboardButton('Пн')
			itembtn2 = types.KeyboardButton('Вт')
			itembtn3 = types.KeyboardButton('Ср')
			itembtn4 = types.KeyboardButton('Чт')
			itembtn5 = types.KeyboardButton('Пт')
			itembtn6 = types.KeyboardButton('Сб')
			itembtn7 = types.KeyboardButton('Вс')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
			
			today_wd = str(current_datetime.strftime("%A"))#week day понедельник
			today_date = str((current_datetime).day)#todays date 23
			isequal = False

			#printing days
			weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
			btn_counter = 1
			i = 0
			size_of_btn_row = 0
			days10 = 0
			while i < 21:
				if(size_of_btn_row<7):
					if(isequal==False and weekdays[i]!=today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						size_of_btn_row+=1
					elif(isequal==False and weekdays[i]==today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(today_date)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(today_date)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(today_date)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(today_date)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(today_date)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(today_date)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(today_date)
						isequal=True
						i+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10<8):
						itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(itembtnday)
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10==8):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
					else:
						print("Not correct ads")
				elif(size_of_btn_row==7):
					markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
					size_of_btn_row = 0
			msg = bot.send_message(message.chat.id, 'День:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_date_edit)
		elif message.text=='Время':
			user = user_dict[message.chat.id]
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Время:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time_edit)
		elif message.text=='Коментарий':
			user = user_dict[message.chat.id]
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('-')
			markup.add(itembtn1)
			msg = bot.send_message(message.chat.id, 'Коментарий:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_comment_edit)
		elif message.text=='Стоимость':
			user = user_dict[message.chat.id]
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
			itembtn1 = types.KeyboardButton('1000')
			itembtn2 = types.KeyboardButton('1500')
			itembtn3 = types.KeyboardButton('2000')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, 'Выберите Стоимость или введите: ', reply_markup=markup)
			bot.register_next_step_handler(msg, process_price_edit)
		else:
			user = user_dict[message.chat.id]
			global fullname
			global phone
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Заказать✅')
			itembtn2 = types.KeyboardButton('Изменить✏️')
			itembtn3 = types.KeyboardButton('Отмена🚫')
			markup.add(itembtn1, itembtn2, itembtn3)
			last_text = '<i><b>' + fullname + '</b></i>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i>\n 🕐: <i><b>' + user.hour+ '</b>\n  ' + user.comment + '</i>'
			msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
			bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_editing!')

def process_name_edit(message):
	try:
		#reading from csv file
		user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		user_new_fullname = message.text
		user_old_fullname = ''
		tel_phone = 0
		global fullname
		global phone
		fullname = message.text
		taxi = ''
		join_date = ''
		users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
		
		for ind in users.index:
			if users['chat_id'][ind]==user_chat_id:
				user_old_fullname = users['fullname'][ind]
				tel_phone = users['phone'][ind]
				join_date = users['join_date'][ind]
				taxi = users['taxi'][ind]
		phone = tel_phone
		users = users[users['chat_id'] != user_chat_id]
		user = pd.DataFrame({"chat_id":[user_chat_id], 
							"fullname":[user_new_fullname],
							"phone":[tel_phone],
							"join_date":[join_date],
							"taxi":[taxi]})
		users = users.append(user, ignore_index=True)
		#writing to scv file
		users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')

		user = user_dict[message.chat.id]
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_name_edit!')

def process_phone_edit(message):
	try:
		if len(message.text) != 11:
			msg = bot.send_message(message.chat.id, 'Длина номера не равен 11. Введите заново.')
			bot.register_next_step_handler(msg, process_phone_edit)
		elif message.text[0] != '8':
			msg = bot.send_message(message.chat.id, 'Номер должен начинаться с 8. Введите заново.')
			bot.register_next_step_handler(msg, process_phone_edit)
		elif message.text[1]!='7':
			msg = bot.send_message(message.chat.id, 'Для операторов РК вторая цифра номера 7. Введите заново.')
			bot.register_next_step_handler(msg, process_phone_edit)
		else:
			try:
				#reading from csv file
				user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
				user_new_phone = message.text
				user_old_phone = 0
				full_name = ''
				global fullname
				global phone
				phone = message.text
				taxi = ''
				join_date = ''
				users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
				
				for ind in users.index:
					if users['chat_id'][ind]==user_chat_id:
						full_name = users['fullname'][ind]
						user_old_phone = users['phone'][ind]
						join_date = users['join_date'][ind]
						taxi = users['taxi'][ind]
				fullname = full_name
				users = users[users['chat_id'] != user_chat_id]
				user = pd.DataFrame({"chat_id":[user_chat_id], 
									"fullname":[full_name],
									"phone":[user_new_phone],
									"join_date":[join_date],
									"taxi":[taxi]})
				users = users.append(user, ignore_index=True)
				#writing to scv file
				users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')

				user = user_dict[message.chat.id]
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Заказать✅')
				itembtn2 = types.KeyboardButton('Изменить✏️')
				itembtn3 = types.KeyboardButton('Отмена🚫')
				markup.add(itembtn1, itembtn2, itembtn3)
				last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
				msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
				bot.register_next_step_handler(msg, process_finishing)
			except Exception as f:
				msg = bot.send_message(message.chat.id, 'Если я не ошибаюсь номер телефона состоит только из цифр.🤔\nВведите заново.')
				bot.register_next_step_handler(msg, process_phone_edit)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_phone_edit!')

def process_from_edit(message):
	try:
		user = user_dict[message.chat.id]
		user.A = message.text
		if user.A == "Шаульдер":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шымкент')
			itembtn2 = types.KeyboardButton('Туркестан')
			itembtn3 = types.KeyboardButton('Алматы')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to_edit)
		elif user.A == "Шымкент":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Туркестан')
			itembtn3 = types.KeyboardButton('Алматы')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to_edit)
		elif user.A == "Туркестан":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Алматы')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to_edit)
		elif user.A == "Алматы":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to_edit)
		elif user.A == "Нур-Султан":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to_edit)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_from_edit!')
def process_to_edit(message):
	try:
		user = user_dict[message.chat.id]
		user.B = message.text
		global fullname
		global phone
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_to_edit!')
def process_date_edit(message):
	try:
		if(int(message.text)<0 or int(message.text)>31):
			f = 0/0
		user = user_dict[message.chat.id]
		user.date = int(message.text)
		global fullname
		global phone
		if(user.date<int((current_datetime).day)):
			month = calendar.month_name[(int(current_datetime.month)+1)]
			if month == 'January':
				month = 'январь'
			elif month == 'February':
				month = 'февраль'
			elif month == 'March':
				month = 'март'
			elif month == 'April':
				month = 'апрель'
			elif month == 'May':
				month = 'май'
			elif month == 'June':
				month = 'июнь'
			elif month == 'July':
				month = 'июль'
			elif month == 'August':
				month = 'август'
			elif month == 'September':
				month = 'сентябрь'
			elif month == 'October':
				month = 'октябрь'
			elif month == 'November':
				month = 'ноябрь'
			elif month == 'December':
				month = 'декабрь'
			user.full_date = str(user.date) + ' ' + str(month)
		elif(user.date>int((current_datetime).day)):
			month = calendar.month_name[int(current_datetime.month)]
			if month == 'January':
				month = 'январь'
			elif month == 'February':
				month = 'февраль'
			elif month == 'March':
				month = 'март'
			elif month == 'April':
				month = 'апрель'
			elif month == 'May':
				month = 'май'
			elif month == 'June':
				month = 'июнь'
			elif month == 'July':
				month = 'июль'
			elif month == 'August':
				month = 'август'
			elif month == 'September':
				month = 'сентябрь'
			elif month == 'October':
				month = 'октябрь'
			elif month == 'November':
				month = 'ноябрь'
			elif month == 'December':
				month = 'декабрь'
			user.full_date = str(user.date) + ' ' + str(month)
		elif(user.date==int(current_datetime.day)):
			user.full_date = 'Сегодня'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		user = user_dict[message.chat.id]
		#printing date of weeks
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
		weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
		# for wd in weekdays:
		month = str((current_datetime).strftime("%B"))
		if month == 'January':
			month = 'Январь'
		elif month == 'February':
			month = 'Февраль'
		elif month == 'March':
			month = 'Март'
		elif month == 'April':
			month = 'Апрель'
		elif month == 'May':
			month = 'Май'
		elif month == 'June':
			month = 'Июнь'
		elif month == 'July':
			month = 'Июль'
		elif month == 'August':
			month = 'Август'
		elif month == 'September':
			month = 'Сентябрь'
		elif month == 'October':
			month = 'Октябрь'
		elif month == 'November':
			month = 'Ноябрь'
		elif month == 'December':
			month = 'Декабрь'
		itembtn = types.KeyboardButton(month)
		markup.add(itembtn)
		itembtn1 = types.KeyboardButton('Пн')
		itembtn2 = types.KeyboardButton('Вт')
		itembtn3 = types.KeyboardButton('Ср')
		itembtn4 = types.KeyboardButton('Чт')
		itembtn5 = types.KeyboardButton('Пт')
		itembtn6 = types.KeyboardButton('Сб')
		itembtn7 = types.KeyboardButton('Вс')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
		
		today_wd = str(current_datetime.strftime("%A"))#week day понедельник
		today_date = str((current_datetime).day)#todays date 23
		isequal = False

		#printing days
		weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		btn_counter = 1
		i = 0
		size_of_btn_row = 0
		days10 = 0
		while i < 21:
			if(size_of_btn_row<7):
				if(isequal==False and weekdays[i]!=today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					size_of_btn_row+=1
				elif(isequal==False and weekdays[i]==today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(today_date)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(today_date)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(today_date)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(today_date)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(today_date)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(today_date)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(today_date)
					isequal=True
					i+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10<8):
					itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(itembtnday)
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10==8):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
				else:
					print("Not correct ads")
			elif(size_of_btn_row==7):
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
				size_of_btn_row = 0
		msg = bot.send_message(message.chat.id, 'Выберите только те дни которые есть в календаре!', reply_markup=markup)
		bot.register_next_step_handler(msg, process_date_edit)

def process_time_edit(message):
	try:
		time = message.text
		if(time[2]!=':'):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time_edit)
		elif(int(time[0:2])>24 or int(time[0:2])<0 or int(time[3:])<0 or int(time[3:])>60):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time_edit)
		else:
			user = user_dict[message.chat.id]
			user.hour = message.text
			global fullname
			global phone
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Заказать✅')
			itembtn2 = types.KeyboardButton('Изменить✏️')
			itembtn3 = types.KeyboardButton('Отмена🚫')
			markup.add(itembtn1, itembtn2, itembtn3)
			last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
			msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
			bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить process_time_edit!')
def process_comment_edit(message):
	try:
		user = user_dict[message.chat.id]
		user.comment = message.text
		global fullname
		global phone
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить process_comment_edit!')
def process_price_edit(message):
	try:
		user = user_dict[message.chat.id]
		user.price = int(message.text)
		if(user.price<0):
			msg = bot.send_message(message.chat.id, 'Цена не может быть отрицательным', reply_markup=markup)
			bot.register_next_step_handler(msg, process_price_edit)
		global fullname
		global phone
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(user.price)+'</b>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.full_date + '</b></i> в <i><b>' + user.hour + '</b>\n  ' + user.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		msg = bot.send_message(message.chat.id, 'Введите только цифры', reply_markup=markup)
		bot.register_next_step_handler(msg, process_price_edit)
#---------------END-EDITING---------------------------------------------------------------------------------------------------------------------

#---------------CANCELING-----------------------------------------------------------------------------------------------------------------------
def process_canceling(message):
	try:
		if message.text=='Отменить заказ🚫':
			msg = bot.send_message(message.chat.id, '🧾 Введите код остановки заказа, для подтверждения: ')
			bot.register_next_step_handler(msg, process_canceling_accept)
		elif message.text=='Пpoдoлжить':
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
			itembtn2 = types.KeyboardButton('/Настройки⚙️')
			markup.add(itembtn1, itembtn2)
			bot.send_message(message.chat.id, "Ваш заказ завершен, можете продолжить.", reply_markup = markup)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		else:
			msg = bot.send_message(message.chat.id, 'Ваш заказ не закончен!')
			bot.register_next_step_handler(msg, process_canceling)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Отменить заказ🚫 process_canceling!')

def process_canceling_accept(message):
	try:
		requests = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
		user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		user_message_id = 0
		user_from = ''
		user_to = ''
		user_price = ''
		user_date = ''
		user_month = ''
		user_year = ''
		user_time = ''
		user_comments = ''
		user_status = 'отменен'
		indices = 0

		for ind in requests.index:
			if ((requests['chat_id'][ind]==user_chat_id) and pd.isnull(requests['status'][ind])):
				indices = ind
				user_message_id = requests['message_id'][ind]
				user_from = requests['from'][ind]
				user_to = requests['to'][ind]
				user_price = requests['price'][ind]
				user_date = requests['day'][ind]
				user_month = requests['month'][ind]
				user_year = requests['year'][ind]
				user_time = requests['time'][ind]
				user_comments = requests['comment'][ind]
		if(str(message.text)==str(user_message_id)):
			bot.delete_message(otyrartaxi_id, int(message.text))
			bot.send_message(message.chat.id, 'Ваш заказ остановлен!')
			requests = requests.drop([indices])
			request = pd.DataFrame({"chat_id":[user_chat_id], 
								"message_id":[user_message_id],
								"from":[user_from],
								"to":[user_to],
								"price": [user_price],
								"day":[user_date],
								"month":[user_month],
								"year":[user_year],
								"time":[user_time],
								"comment":[user_comments],
								"status":[user_status]})
			requests = requests.append(request, ignore_index=True)
			#writing to scv file
			requests.to_csv(r'users_requests.csv', index = False, header=True, encoding='cp1251')

			#deleting from resending_req_driver.csv
			rtd = pd.read_csv('resending_req_driver.csv', sep=',', encoding='cp1251')
			rtds = rtd[rtd['group_message_id']==user_message_id]
			if(rtds.empty==False):
				driver_id = rtds['driver_id'].values
				driver_id = int(driver_id[0])
				message_id = rtds['driver_message_id'].values
				message_id = int(message_id[0])
				bot.delete_message(driver_id, message_id)
				indices = 0
				rtd = rtd[rtd['group_message_id']!=int(user_message_id)]
				rtd.to_csv(r'resending_req_driver.csv', index = False, header=True, encoding='cp1251')

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
			itembtn2 = types.KeyboardButton('/Настройки⚙️')
			markup.add(itembtn1, itembtn2)
			msg = bot.send_message(message.chat.id, "Можете совершать услуги", reply_markup = markup)
		else:
			msg = bot.send_message(message.chat.id, "Код подтверждения не правильный")
			bot.register_next_step_handler(msg, process_canceling_accept)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
		itembtn2 = types.KeyboardButton('/Настройки⚙️')
		markup.add(itembtn1, itembtn2)
		msg = bot.send_message(message.chat.id, "Извините, ошибка.\nЗаполните заново!", reply_markup = markup)
#---------------END-CANCELING---------------------------------------------------------------------------------------------------------------------

#---------------DRIVER-----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['Подтвердить'])
def welcome_driver(message):
	try:
		user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		full_name = ''
		phone = ''
		join_date = ''
		#updating data in client.csv
		users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
		for ind in users.index:
			if (users['chat_id'][ind]==user_chat_id):
				full_name = users['fullname'][ind]
				phone = users['phone'][ind]
				join_date = users['join_date'][ind]
		taxi = 'y'
		users = users[users['chat_id']!=user_chat_id]
		user = pd.DataFrame({"chat_id":[user_chat_id], 
							"fullname":[full_name],
							"phone":[phone],
							"join_date":[join_date],
							"taxi":[taxi]})
		users = users.append(user, ignore_index=True)
		users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')

		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('Добавить заявку➕')
		itembtn2 = types.KeyboardButton('Статистика📈')
		itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
		markup.add(itembtn1, itembtn2, itembtn3)
		msg = bot.send_message(message.chat.id, "Вы в режиме водиетеля!\nВ Статистика📈 можете посмотреть статистику запросов от клиентов", reply_markup = markup)
		bot.register_next_step_handler(msg, chosing_diver)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить accept_driver!')
def chosing_diver(message):
	try:
		if message.text == 'Добавить заявку➕':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			itembtn5 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

			msg = bot.send_message(message.chat.id, 'Откуда(точка A)?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_from)
		elif message.text == 'Стать Пассажиром👤':
			#reading from csv file
			user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
			user_phone = 0
			full_name = ''
			global fullname
			global phone
			phone = message.text
			taxi = 'n'
			join_date = ''
			users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
			for ind in users.index:
				if users['chat_id'][ind]==user_chat_id:
					full_name = users['fullname'][ind]
					user_phone = users['phone'][ind]
					join_date = users['join_date'][ind]
			fullname = full_name
			users = users[users['chat_id'] != user_chat_id]
			user = pd.DataFrame({"chat_id":[user_chat_id], 
								"fullname":[full_name],
								"phone":[user_phone],
								"join_date":[join_date],
								"taxi":[taxi]})
			users = users.append(user, ignore_index=True)
			#writing to scv file
			users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')
			sti = open('static/client.webp', 'rb')
			bot.send_sticker(message.chat.id, sti)
			sti.close()
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Новый_Заказ🟢')
			itembtn2 = types.KeyboardButton('/Настройки⚙️')
			markup.add(itembtn1, itembtn2)
			msg = bot.send_message(message.chat.id, "Вы в режиме клиента, совершайте услуги!", reply_markup = markup)
		elif message.text == 'Статистика📈':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Активность по времени')
			itembtn2 = types.KeyboardButton('Активность по городам')
			itembtn3 = types.KeyboardButton('Активность по дням недели')
			itembtn4 = types.KeyboardButton('🔙Назад')

			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

			msg = bot.send_message(message.chat.id, 'Выберите статистику', reply_markup=markup)
			bot.register_next_step_handler(msg, get_statistic)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "", reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить chosing_diver!')
def process_driver_from(message):
	try:
		if message.text=='Шаульдер' or message.text=='Шымкент' or message.text=='Туркестан' or message.text=='Алматы' or message.text=='Нур-Султан':
			#new_data
			driver_dict[message.chat.id] = Driver(message.text)
			
			if message.text == "Шаульдер":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шымкент')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif message.text == "Шымкент":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif message.text == "Туркестан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif message.text == "Алматы":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif message.text == "Нур-Султан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Алматы')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			itembtn5 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, 'Выберите только из списка!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_to)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_driver_from!')
def process_driver_date(message):
	try:
		if message.text=='Шаульдер' or message.text=='Шымкент' or message.text=='Туркестан' or message.text=='Алматы' or message.text=='Нур-Султан':
			driver = driver_dict[message.chat.id]
			driver.B = message.text
			#printing date of weeks
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
			weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
			# for wd in weekdays:
			month = str((current_datetime).strftime("%B"))
			if month == 'January':
				month = 'Январь'
			elif month == 'February':
				month = 'Февраль'
			elif month == 'March':
				month = 'Март'
			elif month == 'April':
				month = 'Апрель'
			elif month == 'May':
				month = 'Май'
			elif month == 'June':
				month = 'Июнь'
			elif month == 'July':
				month = 'Июль'
			elif month == 'August':
				month = 'Август'
			elif month == 'September':
				month = 'Сентябрь'
			elif month == 'October':
				month = 'Октябрь'
			elif month == 'November':
				month = 'Ноябрь'
			elif month == 'December':
				month = 'Декабрь'
			itembtn = types.KeyboardButton(month)
			markup.add(itembtn)
			itembtn1 = types.KeyboardButton('Пн')
			itembtn2 = types.KeyboardButton('Вт')
			itembtn3 = types.KeyboardButton('Ср')
			itembtn4 = types.KeyboardButton('Чт')
			itembtn5 = types.KeyboardButton('Пт')
			itembtn6 = types.KeyboardButton('Сб')
			itembtn7 = types.KeyboardButton('Вс')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
			
			today_wd = str(current_datetime.strftime("%A"))#week day понедельник
			today_date = str((current_datetime).day)#todays date 23
			isequal = False

			#printing days
			weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
			btn_counter = 1
			i = 0
			size_of_btn_row = 0
			days10 = 0
			while i < 21:
				if(size_of_btn_row<7):
					if(isequal==False and weekdays[i]!=today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						size_of_btn_row+=1
					elif(isequal==False and weekdays[i]==today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(today_date)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(today_date)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(today_date)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(today_date)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(today_date)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(today_date)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(today_date)
						isequal=True
						i+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10<8):
						itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(itembtnday)
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10==8):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
					else:
						print("Not correct ads")
				elif(size_of_btn_row==7):
					markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
					size_of_btn_row = 0
			msg = bot.send_message(message.chat.id, 'Выберите только те дни которые есть в календаре!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_time)
		else:
			driver = driver_dict[message.chat.id]
			if driver.A == "Шаульдер":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шымкент')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif driver.A == "Шымкент":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif driver.A == "Туркестан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif driver.A == "Алматы":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
			elif driver.A == "Нур-Султан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Алматы')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_date)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_driver_date!')

def process_driver_time(message):
	try:
		if(int(message.text)<0 or int(message.text)>31):
			f = 0/0
		driver = driver_dict[message.chat.id]
		driver.date = int(message.text)
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
		if int(driver.date)==int(current_datetime.day):
			current_hour = int(current_datetime.hour)
			current_minute = int(current_datetime.minute)
			if(current_minute >= 30):
				current_minute = '00'
				current_hour+=1
			else:
				current_minute = '30'
			butnequaltf = False
			while current_hour!=24:
				print_time1 = ''
				print_time2 = ''
				if(current_hour<10):
					print_time1 = '0'+str(current_hour)+':'+current_minute
					if current_minute=='30':
						current_hour+=1
						current_minute = '00'
					elif current_minute=='00':
						current_minute = '30'
					if(current_hour<10):
						print_time2 = '0'+str(current_hour)+':'+current_minute
						if current_minute=='30':
							current_hour+=1
							current_minute = '00'
						elif current_minute=='00':
							current_minute = '30'
				elif(current_hour>=10):
					print_time1 = str(current_hour)+':'+current_minute
					if current_minute=='30':
						current_hour+=1
						current_minute = '00'
					elif current_minute=='00':
						current_minute = '30'
					if(current_hour>=10 and current_hour!=24):
						print_time2 = str(current_hour)+':'+current_minute
						if current_minute=='30':
							current_hour+=1
							current_minute = '00'
						elif current_minute=='00':
							current_minute = '30'
					else:
						butnequaltf = True
				if(butnequaltf==False):
					itembtn1 = types.KeyboardButton(print_time1)
					itembtn2 = types.KeyboardButton(print_time2)
					markup.add(itembtn1, itembtn2)
				elif(butnequaltf==True):
					itembtn1 = types.KeyboardButton(print_time1)
					markup.add(itembtn1)
		else:
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
		msg = bot.send_message(message.chat.id, 'Время:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_driver_comment)
	except Exception as e:
		driver = driver_dict[message.chat.id]
		#printing date of weeks
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
		weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
		# for wd in weekdays:
		month = str((current_datetime).strftime("%B"))
		if month == 'January':
			month = 'Январь'
		elif month == 'February':
			month = 'Февраль'
		elif month == 'March':
			month = 'Март'
		elif month == 'April':
			month = 'Апрель'
		elif month == 'May':
			month = 'Май'
		elif month == 'June':
			month = 'Июнь'
		elif month == 'July':
			month = 'Июль'
		elif month == 'August':
			month = 'Август'
		elif month == 'September':
			month = 'Сентябрь'
		elif month == 'October':
			month = 'Октябрь'
		elif month == 'November':
			month = 'Ноябрь'
		elif month == 'December':
			month = 'Декабрь'
		itembtn = types.KeyboardButton(month)
		markup.add(itembtn)
		itembtn1 = types.KeyboardButton('Пн')
		itembtn2 = types.KeyboardButton('Вт')
		itembtn3 = types.KeyboardButton('Ср')
		itembtn4 = types.KeyboardButton('Чт')
		itembtn5 = types.KeyboardButton('Пт')
		itembtn6 = types.KeyboardButton('Сб')
		itembtn7 = types.KeyboardButton('Вс')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
		
		today_wd = str(current_datetime.strftime("%A"))#week day ex: Monday
		today_date = str((current_datetime).day)#todays date ex: 23
		isequal = False

		#printing days
		weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		btn_counter = 1
		i = 0
		size_of_btn_row = 0
		days10 = 0
		while i < 21:
			if(size_of_btn_row<7):
				if(isequal==False and weekdays[i]!=today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					size_of_btn_row+=1
				elif(isequal==False and weekdays[i]==today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(today_date)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(today_date)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(today_date)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(today_date)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(today_date)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(today_date)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(today_date)
					isequal=True
					i+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10<8):
					itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(itembtnday)
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10==8):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
				else:
					print("Not correct ads")
			elif(size_of_btn_row==7):
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
				size_of_btn_row = 0
		msg = bot.send_message(message.chat.id, 'Выберите только те дни которые есть в календаре!', reply_markup=markup)
		bot.register_next_step_handler(msg, process_driver_time)

def process_driver_comment(message):
	try:
		time = message.text
		if(time[2]!=':'):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_comment)
		elif(int(time[0:2])>24 or int(time[0:2])<0 or int(time[3:])<0 or int(time[3:])>60):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_comment)
		else:
			driver = driver_dict[message.chat.id]
			driver.hour = message.text
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('-')
			markup.add(itembtn1)
			msg = bot.send_message(message.chat.id, 'Коментарий:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_price)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_driver_comment!')
def process_driver_price(message):
	try:
		driver = driver_dict[message.chat.id]
		driver.comment = message.text
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
		itembtn1 = types.KeyboardButton('1000')
		itembtn2 = types.KeyboardButton('1500')
		itembtn3 = types.KeyboardButton('2000')
		markup.add(itembtn1, itembtn2, itembtn3)
		msg = bot.send_message(message.chat.id, 'Выберите Стоимость или введите: ', reply_markup=markup)
		bot.register_next_step_handler(msg, process_driver_prefinishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Новый_Заказ🟢 process_price!')
#---------------finishing of NEW_REQUEST---------------
def process_driver_prefinishing(message):
	try:
		try:
			driver = driver_dict[message.chat.id]
			driver.price = int(message.text)
			if(driver.price<0):
				msg = bot.send_message(message.chat.id, 'Цена не может быть отрицательным! Выберите или введите заново.')
				bot.register_next_step_handler(msg, process_driver_prefinishing)
			else:
				#getting fullname and phone from client.csv file
				global fullname
				global phone
				users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
				fn = users[users['chat_id']==message.chat.id]['fullname'].values
				fullname = fn[0]
				ph = users[users['chat_id']==message.chat.id]['phone'].values
				phone = ph[0]

				if(driver.date<int((current_datetime).day)):
					driver.month = str(int(current_datetime.month)+1)
					month = calendar.month_name[(int(current_datetime.month)+1)]
					if month == 'January':
						month = 'янв.'
					elif month == 'February':
						month = 'фев.'
					elif month == 'March':
						month = 'мар.'
					elif month == 'April':
						month = 'апр.'
					elif month == 'May':
						month = 'май'
					elif month == 'June':
						month = 'июн.'
					elif month == 'July':
						month = 'июл.'
					elif month == 'August':
						month = 'авг.'
					elif month == 'September':
						month = 'сен.'
					elif month == 'October':
						month = 'окт.'
					elif month == 'November':
						month = 'ноя.'
					elif month == 'December':
						month = 'дек.'
					driver.full_date = str(driver.date)+' '+str(month)
				elif(driver.date>int((current_datetime).day)):
					driver.month = str(current_datetime.month)
					month = calendar.month_name[int(current_datetime.month)]
					if month == 'January':
						month = 'янв.'
					elif month == 'February':
						month = 'фев.'
					elif month == 'March':
						month = 'мар.'
					elif month == 'April':
						month = 'апр.'
					elif month == 'May':
						month = 'май'
					elif month == 'June':
						month = 'июн.'
					elif month == 'July':
						month = 'июл.'
					elif month == 'August':
						month = 'авг.'
					elif month == 'September':
						month = 'сен.'
					elif month == 'October':
						month = 'окт.'
					elif month == 'November':
						month = 'ноя.'
					elif month == 'December':
						month = 'дек.'
					driver.full_date = str(driver.date)+' '+str(month)
				elif(driver.date==int(current_datetime.day)):
					driver.month = str(current_datetime.month)
					driver.full_date = 'Сегодня'
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Заказать✅')
				itembtn2 = types.KeyboardButton('Изменить✏️')
				itembtn3 = types.KeyboardButton('Отмена🚫')

				markup.add(itembtn1, itembtn2, itembtn3)
				last_text = '<i><b>' + fullname + '</b></i>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour+ '</b>\n  ' + driver.comment + '</i>'
				msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
				bot.register_next_step_handler(msg, process_driver_finishing)
		except Exception as e:
			msg = bot.send_message(message.chat.id, 'Введите только цифры')
			bot.register_next_step_handler(msg, process_driver_prefinishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_prefinishing!')

def process_driver_finishing(message):
	try:
		global fullname
		global phone
		driver = driver_dict[message.chat.id]
		user_chat_id = message.chat.id
		user_from = driver.A
		user_to = driver.B
		user_price = driver.price
		user_time = driver.hour
		user_comment = driver.comment
		user_date = str(driver.date)
		user_month = str(driver.month)
		user_year = str(current_datetime.year)
		user_status = ''
		user_message_id = 0
		if message.text=='Заказать✅':
			last_text = '<b>TAXI, ' + str(driver.price) + '</b>\n👤:  <a href="tg://user?id={0.id}">' + fullname + '</a>, ' + str(phone) + '\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
			msg = bot.send_message(otyrartaxi_id, last_text.format(message.from_user, bot.get_me()), parse_mode='html')
			user_message_id = int(msg.id)

			requests_df = pd.read_csv('drivers_requests.csv', sep=',', encoding="cp1251")
			request = pd.DataFrame({"chat_id":[user_chat_id],
									"message_id":[user_message_id],
									"from":[user_from],
									"to":[user_to],
									"price":[user_price],
									"day":[user_date],
									"month":[user_month],
									"year":[user_year],
									"time":[user_time],
									"comment":[user_comment],
									"status":[user_status]})
			requests_df = requests_df.append(request, ignore_index=True)
			#writing to scv file
			requests_df.to_csv(r'drivers_requests.csv', index = False, header=True, encoding='cp1251')
				#~~~sending requests from me to other clients --AND-- from other clietns to me
			is_requests = False #to check is there only online requests
			resending_to_users = pd.read_csv('resending_req_user.csv', sep=',', encoding='cp1251')
			resending_to_me_driver = pd.read_csv('resending_req_driver.csv', sep=',', encoding='cp1251')
				#~~~to check online requests
			users_requests = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
				#~~~to get is user taxi or not and get phone
			users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
			for ind in users.index:
				if (users['taxi'][ind]=='n'):
					user_reqs = users_requests[users_requests['chat_id']==users['chat_id'][ind]]
					user_reqs = user_reqs[pd.isnull(user_reqs['status'])]
					user_reqs = user_reqs[user_reqs['from']==driver.A]
					user_reqs = user_reqs[user_reqs['to']==driver.B]
					user_reqs = user_reqs[user_reqs['day']==int(user_date)]
					user_reqs = user_reqs[user_reqs['month']==int(user_month)]
					if(user_reqs.empty==False):
						user_id = int(users['chat_id'][ind])
						to_user_message_id = user_reqs['message_id'].values
						to_user_message_id = int(to_user_message_id[0])
						d_fullname = users['fullname'][ind]
						d_phone = users['phone'][ind]
						d_A = user_reqs['from'].values
						d_A = d_A[0]
						d_B = user_reqs['to'].values
						d_B = d_B[0]
						d_price = user_reqs['price'].values
						d_price = d_price[0]
						d_date = user_reqs['day'].values
						d_date = d_date[0]
						d_month = user_reqs['month'].values
						d_month = d_month[0]
						d_time = user_reqs['time'].values
						d_time = d_time[0]
						d_comment = user_reqs['comment'].values
						d_comment = d_comment[0]
						#------------------------------------------
						#send my request to other online clients 
						msg = bot.send_message(int(user_id), last_text.format(message.from_user, bot.get_me()), parse_mode='html')
						res_to_user = pd.DataFrame({"chat_id":[user_chat_id],#from me
													"group_message_id":[user_message_id],
													"user_id":[user_id],#to clients
													"to_user_message_id":[msg.id]})
						resending_to_users = resending_to_users.append(res_to_user, ignore_index=True)
						resending_to_users.to_csv(r'resending_req_user.csv', index = False, header=True, encoding='cp1251')
						#------------------------------------------
						#send other client online requests to me, text to me driver
						text_to_me_driver = '<b>КЛИЕНТ, ' + str(d_price) + '</b>\n👤: <a href="tg://user?id='+str(user_id)+'">' + d_fullname + '</a>, ' + str(d_phone) + '\n A:  <i><b>' + d_A + '</b></i>\n B:  <i><b>' + d_B + '</b></i>\n 📅: <i><b>' + str(d_date)+'/'+str(d_month) + '</b></i> в <i><b>' + d_time + '</b>\n  ' + d_comment + '</i>'
						
						msg = bot.send_message(message.chat.id, text_to_me_driver, parse_mode='html')
						res_to_me = pd.DataFrame({"chat_id":[user_id],#from clients
													"group_message_id":[to_user_message_id],
													"driver_id":[user_chat_id],#to me
													"driver_message_id":[msg.id]})
						resending_to_me_driver = resending_to_me_driver.append(res_to_me, ignore_index=True)
						resending_to_me_driver.to_csv(r'resending_req_driver.csv', index = False, header=True, encoding='cp1251')
						is_requests = True
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Отменить заказ🚫')
			markup.add(itembtn1)	
			if(is_requests==False):
				msg = bot.send_message(message.chat.id, '🎟️ Ваш заказ добавлен!\n🧾 Код остановки заказа: ' + str(user_message_id), reply_markup=markup)
				msg = bot.send_message(message.chat.id, ' Ждите, пока нету клиентов по вашему маршруту в данный день. Если появятся клиенты по вашему маршруту я вам отправлю. Будьте онлайн, чтобы не пропустить клиента!')
				bot.register_next_step_handler(msg, process_driver_req_canceling)
			else:
				msg = bot.send_message(message.chat.id, '🎟️ Ваш заявка добавлен!\n Вот список клиентов по вашему маршруту, если появятся еще я вам отправлю. Будьте онлайн, чтобы не пропустить клиентов!\n🧾 Код остановки заказа: ' + str(user_message_id), reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_req_canceling)
		elif message.text=='Изменить✏️':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Имя')
			itembtn2 = types.KeyboardButton('Номер')
			itembtn3 = types.KeyboardButton('A')
			itembtn4 = types.KeyboardButton('B')
			itembtn5 = types.KeyboardButton('День')
			itembtn6 = types.KeyboardButton('Время')
			itembtn7 = types.KeyboardButton('Коментарий')
			itembtn8 = types.KeyboardButton('Стоимость')
			itembtn9 = types.KeyboardButton('⬅️НАЗАД')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9)
			msg = bot.send_message(message.chat.id, 'Что хотите изменять?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_req_editing)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "{0.first_name} чтобы заказать нажмите на кнопку ниже".format(message.from_user, bot.get_me()), reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_driver_finishing!')
#---------------END-NEW_REQUEST---------------------------------------------------------------------------------------------------------------

def process_driver_req_editing(message):
	try:
		#удалить старую клавиатуру
		markup = types.ReplyKeyboardRemove(selective=False)
		if message.text=='Имя':
			msg = bot.send_message(message.chat.id, 'Введите имя: ')
			bot.register_next_step_handler(msg, process_driver_name_edit)
		elif message.text=='Номер':
			msg = bot.send_message(message.chat.id, 'Введите номер \nПример: 87771234656')
			bot.register_next_step_handler(msg, process_driver_phone_edit)
		elif message.text=='A':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			itembtn5 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

			msg = bot.send_message(message.chat.id, 'Выберите точку А!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_from_edit)
		elif message.text=='B':
			driver = driver_dict[message.chat.id]
			if user.A == "Шаульдер":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шымкент')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_to_edit)
			elif user.A == "Шымкент":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Туркестан')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_to_edit)
			elif user.A == "Туркестан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Алматы')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_to_edit)
			elif user.A == "Алматы":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Нур-Султан')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				msg = bot.send_message(message.chat.id, 'Куда(точка B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_driver_to_edit)
			elif user.A == "Нур-Султан":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
				itembtn1 = types.KeyboardButton('Шаульдер')
				itembtn2 = types.KeyboardButton('Шымкент')
				itembtn3 = types.KeyboardButton('Туркестан')
				itembtn4 = types.KeyboardButton('Алматы')
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
				bot.register_next_step_handler(msg, process_driver_to_edit)
		elif message.text=='День':
			driver = driver_dict[message.chat.id]
			#printing date of weeks
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
			weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
			# for wd in weekdays:
			itembtn = types.KeyboardButton(str((current_datetime).strftime("%B")))
			markup.add(itembtn)
			itembtn1 = types.KeyboardButton('Пн')
			itembtn2 = types.KeyboardButton('Вт')
			itembtn3 = types.KeyboardButton('Ср')
			itembtn4 = types.KeyboardButton('Чт')
			itembtn5 = types.KeyboardButton('Пт')
			itembtn6 = types.KeyboardButton('Сб')
			itembtn7 = types.KeyboardButton('Вс')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
			
			today_wd = str(current_datetime.strftime("%A"))#week day понедельник
			today_date = str((current_datetime).day)#todays date 23
			isequal = False

			#printing days
			weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
			btn_counter = 1
			i = 0
			size_of_btn_row = 0
			days10 = 0
			while i < 21:
				if(size_of_btn_row<7):
					if(isequal==False and weekdays[i]!=today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						size_of_btn_row+=1
					elif(isequal==False and weekdays[i]==today_wd):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(today_date)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(today_date)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(today_date)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(today_date)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(today_date)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(today_date)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(today_date)
						isequal=True
						i+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10<8):
						itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(itembtnday)
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(itembtnday)
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
						days10+=1
					elif(isequal==True and days10==8):
						if size_of_btn_row==0:
							itembtn1 = types.KeyboardButton(' ')
						elif size_of_btn_row==1:
							itembtn2 = types.KeyboardButton(' ')
						elif size_of_btn_row==2:
							itembtn3 = types.KeyboardButton(' ')
						elif size_of_btn_row==3:
							itembtn4 = types.KeyboardButton(' ')
						elif size_of_btn_row==4:
							itembtn5 = types.KeyboardButton(' ')
						elif size_of_btn_row==5:
							itembtn6 = types.KeyboardButton(' ')
						elif size_of_btn_row==6:
							itembtn7 = types.KeyboardButton(' ')
						i+=1
						btn_counter+=1
						size_of_btn_row+=1
					else:
						print("Not correct ads")
				elif(size_of_btn_row==7):
					markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
					size_of_btn_row = 0
			msg = bot.send_message(message.chat.id, 'День:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_date_edit)
		elif message.text=='Время':
			driver = driver_dict[message.chat.id]
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Время:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_time_edit)
		elif message.text=='Коментарий':
			driver = driver_dict[message.chat.id]
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('-')
			markup.add(itembtn1)
			msg = bot.send_message(message.chat.id, 'Коментарий:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_comment_edit)
		elif message.text=='Стоимость':
			driver = driver_dict[message.chat.id]
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=3)
			itembtn1 = types.KeyboardButton('1000')
			itembtn2 = types.KeyboardButton('1500')
			itembtn3 = types.KeyboardButton('2000')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, 'Выберите Стоимость или введите: ', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_price_edit)
		else:
			driver = driver_dict[message.chat.id]
			global fullname
			global phone
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Заказать✅')
			itembtn2 = types.KeyboardButton('Изменить✏️')
			itembtn3 = types.KeyboardButton('Отмена🚫')
			markup.add(itembtn1, itembtn2, itembtn3)
			last_text = '<i><b>' + fullname + '</b></i>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i>\n 🕐: <i><b>' + driver.hour+ '</b>\n  ' + driver.comment + '</i>'
			msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
			bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_driver_req_editing!')

def process_driver_name_edit(message):
	try:
		#reading from csv file
		user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		user_new_fullname = message.text
		user_old_fullname = ''
		tel_phone = 0
		global fullname
		global phone
		fullname = message.text
		taxi = ''
		join_date = ''
		users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
		
		for ind in users.index:
			if users['chat_id'][ind]==user_chat_id:
				user_old_fullname = users['fullname'][ind]
				tel_phone = users['phone'][ind]
				join_date = users['join_date'][ind]
				taxi = users['taxi'][ind]
		phone = tel_phone
		users = users[users['chat_id'] != user_chat_id]
		user = pd.DataFrame({"chat_id":[user_chat_id], 
							"fullname":[user_new_fullname],
							"phone":[tel_phone],
							"join_date":[join_date],
							"taxi":[taxi]})
		users = users.append(user, ignore_index=True)
		#writing to scv file
		users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')

		driver = driver_dict[message.chat.id]
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_driver_name_edit!')

def process_driver_phone_edit(message):
	try:
		if len(message.text) != 11:
			msg = bot.send_message(message.chat.id, 'Длина номера не равен 11. Введите заново.')
			bot.register_next_step_handler(msg, process_driver_phone_edit)
		elif message.text[0] != '8':
			msg = bot.send_message(message.chat.id, 'Номер должен начинаться с 8. Введите заново.')
			bot.register_next_step_handler(msg, process_driver_phone_edit)
		elif message.text[1]!='7':
			msg = bot.send_message(message.chat.id, 'Для операторов РК вторая цифра номера 7. Введите заново.')
			bot.register_next_step_handler(msg, process_driver_phone_edit)
		else:
			try:
				#reading from csv file
				user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
				user_new_phone = message.text
				user_old_phone = 0
				full_name = ''
				global fullname
				global phone
				phone = message.text
				taxi = ''
				join_date = ''
				users = pd.read_csv('users.csv', sep=',', encoding='cp1251')
				
				for ind in users.index:
					if users['chat_id'][ind]==user_chat_id:
						full_name = users['fullname'][ind]
						user_old_phone = users['phone'][ind]
						join_date = users['join_date'][ind]
						taxi = users['taxi'][ind]
				fullname = full_name
				users = users[users['chat_id'] != user_chat_id]
				user = pd.DataFrame({"chat_id":[user_chat_id], 
									"fullname":[full_name],
									"phone":[user_new_phone],
									"join_date":[join_date],
									"taxi":[taxi]})
				users = users.append(user, ignore_index=True)
				#writing to scv file
				users.to_csv(r'users.csv', index = False, header=True, encoding='cp1251')

				driver = driver_dict[message.chat.id]
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Заказать✅')
				itembtn2 = types.KeyboardButton('Изменить✏️')
				itembtn3 = types.KeyboardButton('Отмена🚫')
				markup.add(itembtn1, itembtn2, itembtn3)
				last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
				msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
				bot.register_next_step_handler(msg, process_driver_finishing)
			except Exception as f:
				msg = bot.send_message(message.chat.id, 'Если я не ошибаюсь номер телефона состоит только из цифр.🤔\nВведите заново.')
				bot.register_next_step_handler(msg, process_driver_phone_edit)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_driver_phone_edit!')

def process_driver_from_edit(message):
	try:
		driver = driver_dict[message.chat.id]
		driver.A = message.text
		if driver.A == "Шаульдер":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шымкент')
			itembtn2 = types.KeyboardButton('Туркестан')
			itembtn3 = types.KeyboardButton('Алматы')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_to_edit)
		elif driver.A == "Шымкент":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Туркестан')
			itembtn3 = types.KeyboardButton('Алматы')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_to_edit)
		elif driver.A == "Туркестан":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Алматы')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_to_edit)
		elif driver.A == "Алматы":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Нур-Султан')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_to_edit)
		elif driver.A == "Нур-Султан":
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			itembtn1 = types.KeyboardButton('Шаульдер')
			itembtn2 = types.KeyboardButton('Шымкент')
			itembtn3 = types.KeyboardButton('Туркестан')
			itembtn4 = types.KeyboardButton('Алматы')
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
			msg = bot.send_message(message.chat.id, 'Выберите точку В!?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_to_edit)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_driver_from_edit!')
def process_driver_to_edit(message):
	try:
		driver = driver_dict[message.chat.id]
		driver.B = message.text
		global fullname
		global phone
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить✏️ process_driver_to_edit!')
def process_driver_date_edit(message):
	try:
		if(int(message.text)<0 or int(message.text)>31):
			f = 0/0
		driver = driver_dict[message.chat.id]
		driver.date = int(message.text)
		global fullname
		global phone
		if(driver.date<int((current_datetime).day)):
			month = calendar.month_name[(int(current_datetime.month)+1)]
			if month == 'January':
				month = 'январь'
			elif month == 'February':
				month = 'февраль'
			elif month == 'March':
				month = 'март'
			elif month == 'April':
				month = 'апрель'
			elif month == 'May':
				month = 'май'
			elif month == 'June':
				month = 'июнь'
			elif month == 'July':
				month = 'июль'
			elif month == 'August':
				month = 'август'
			elif month == 'September':
				month = 'сентябрь'
			elif month == 'October':
				month = 'октябрь'
			elif month == 'November':
				month = 'ноябрь'
			elif month == 'December':
				month = 'декабрь'
			driver.full_date = str(driver.date) + ' ' + str(month)
		elif(driver.date>int((current_datetime).day)):
			month = calendar.month_name[int(current_datetime.month)]
			if month == 'January':
				month = 'январь'
			elif month == 'February':
				month = 'февраль'
			elif month == 'March':
				month = 'март'
			elif month == 'April':
				month = 'апрель'
			elif month == 'May':
				month = 'май'
			elif month == 'June':
				month = 'июнь'
			elif month == 'July':
				month = 'июль'
			elif month == 'August':
				month = 'август'
			elif month == 'September':
				month = 'сентябрь'
			elif month == 'October':
				month = 'октябрь'
			elif month == 'November':
				month = 'ноябрь'
			elif month == 'December':
				month = 'декабрь'
			driver.full_date = str(driver.date) + ' ' + str(month)
		elif(driver.date==int(current_datetime.day)):
			driver.full_date = 'Сегодня'
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		driver = driver_dict[message.chat.id]
		#printing date of weeks
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=7)
		weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс' ]
		# for wd in weekdays:
		month = str((current_datetime).strftime("%B"))
		if month == 'January':
			month = 'Январь'
		elif month == 'February':
			month = 'Февраль'
		elif month == 'March':
			month = 'Март'
		elif month == 'April':
			month = 'Апрель'
		elif month == 'May':
			month = 'Май'
		elif month == 'June':
			month = 'Июнь'
		elif month == 'July':
			month = 'Июль'
		elif month == 'August':
			month = 'Август'
		elif month == 'September':
			month = 'Сентябрь'
		elif month == 'October':
			month = 'Октябрь'
		elif month == 'November':
			month = 'Ноябрь'
		elif month == 'December':
			month = 'Декабрь'
		itembtn = types.KeyboardButton(month)
		markup.add(itembtn)
		itembtn1 = types.KeyboardButton('Пн')
		itembtn2 = types.KeyboardButton('Вт')
		itembtn3 = types.KeyboardButton('Ср')
		itembtn4 = types.KeyboardButton('Чт')
		itembtn5 = types.KeyboardButton('Пт')
		itembtn6 = types.KeyboardButton('Сб')
		itembtn7 = types.KeyboardButton('Вс')
		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
		
		today_wd = str(current_datetime.strftime("%A"))#week day понедельник
		today_date = str((current_datetime).day)#todays date 23
		isequal = False

		#printing days
		weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		btn_counter = 1
		i = 0
		size_of_btn_row = 0
		days10 = 0
		while i < 21:
			if(size_of_btn_row<7):
				if(isequal==False and weekdays[i]!=today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					size_of_btn_row+=1
				elif(isequal==False and weekdays[i]==today_wd):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(today_date)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(today_date)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(today_date)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(today_date)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(today_date)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(today_date)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(today_date)
					isequal=True
					i+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10<8):
					itembtnday = str((current_datetime + timedelta(days=btn_counter)).day)
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(itembtnday)
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(itembtnday)
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
					days10+=1
				elif(isequal==True and days10==8):
					if size_of_btn_row==0:
						itembtn1 = types.KeyboardButton(' ')
					elif size_of_btn_row==1:
						itembtn2 = types.KeyboardButton(' ')
					elif size_of_btn_row==2:
						itembtn3 = types.KeyboardButton(' ')
					elif size_of_btn_row==3:
						itembtn4 = types.KeyboardButton(' ')
					elif size_of_btn_row==4:
						itembtn5 = types.KeyboardButton(' ')
					elif size_of_btn_row==5:
						itembtn6 = types.KeyboardButton(' ')
					elif size_of_btn_row==6:
						itembtn7 = types.KeyboardButton(' ')
					i+=1
					btn_counter+=1
					size_of_btn_row+=1
				else:
					print("Not correct ads")
			elif(size_of_btn_row==7):
				markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
				size_of_btn_row = 0
		msg = bot.send_message(message.chat.id, 'Выберите только те дни которые есть в календаре!', reply_markup=markup)
		bot.register_next_step_handler(msg, process_driver_date_edit)

def process_driver_time_edit(message):
	try:
		time = message.text
		if(time[2]!=':'):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_time_edit)
		elif(int(time[0:2])>24 or int(time[0:2])<0 or int(time[3:])<0 or int(time[3:])>60):
			time_list = ['06:00','06:30','07:00','07:30','08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00','12:30','13:00','13:30','14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30','21:00','21:30','22:00','22:30','23:00','23:30','00:00','00:30','01:00','01:30','02:00','02:30','03:00','03:30','04:00','04:30','05:00','05:30']
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
			i=0
			while i < 48:
				itembtn1 = types.KeyboardButton(time_list[i])
				itembtn2 = types.KeyboardButton(time_list[i+1])
				markup.add(itembtn1, itembtn2)
				i+=2
			msg = bot.send_message(message.chat.id, 'Вы не ввели время, выберите время!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_time_edit)
		else:
			driver = driver_dict[message.chat.id]
			driver.hour = message.text
			global fullname
			global phone
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Заказать✅')
			itembtn2 = types.KeyboardButton('Изменить✏️')
			itembtn3 = types.KeyboardButton('Отмена🚫')
			markup.add(itembtn1, itembtn2, itembtn3)
			last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
			msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
			bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить process_driver_time_edit!')
def process_driver_comment_edit(message):
	try:
		driver = driver_dict[message.chat.id]
		driver.comment = message.text
		global fullname
		global phone
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Изменить process_driver_comment_edit!')
def process_driver_price_edit(message):
	try:
		driver = driver_dict[message.chat.id]
		driver.price = int(message.text)
		if(driver.price<0):
			msg = bot.send_message(message.chat.id, 'Цена не может быть отрицательным', reply_markup=markup)
			bot.register_next_step_handler(msg, process_driver_price_edit)
		global fullname
		global phone
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Заказать✅')
		itembtn2 = types.KeyboardButton('Изменить✏️')
		itembtn3 = types.KeyboardButton('Отмена🚫')
		markup.add(itembtn1, itembtn2, itembtn3)
		last_text = '<b><i>' + fullname + '</i></b>, Ваш заказ: \n 📞: <i><b>' + str(phone) + '</b></i>\n 💸: <b>'+str(driver.price)+'</b>\n A:  <i><b>' + driver.A + '</b></i>\n B:  <i><b>' + driver.B + '</b></i>\n 📅: <i><b>' + driver.full_date + '</b></i> в <i><b>' + driver.hour + '</b>\n  ' + driver.comment + '</i>'
		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_driver_finishing)
	except Exception as e:
		msg = bot.send_message(message.chat.id, 'Введите только цифры', reply_markup=markup)
		bot.register_next_step_handler(msg, process_driver_price_edit)
#---------------END-EDITING---------------------------------------------------------------------------------------------------------------------


#---------------CANCELING-----------------------------------------------------------------------------------------------------------------------
def process_driver_req_canceling(message):
	try:
		if message.text=='Отменить заказ🚫':
			msg = bot.send_message(message.chat.id, '🧾 Введите код остановки заказа, для подтверждения: ')
			bot.register_next_step_handler(msg, process_driver_req_canceling_accept)
		elif message.text=='Пpoдолжить':#this `Продолжить` have different letters than previus `Продолжить` in user request
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			bot.send_message(message.chat.id, "Ваш заказ завершен, можете продолжить.", reply_markup = markup)
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		else:
			msg = bot.send_message(message.chat.id, 'Ваш заказ не закончен!')
			bot.register_next_step_handler(msg, process_driver_req_canceling_accept)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Подтвердить process_driver_req_canceling!')

def process_driver_req_canceling_accept(message):
	try:
		requests = pd.read_csv('drivers_requests.csv', sep=',', encoding='cp1251')
		user_chat_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		user_message_id = 0
		user_from = ''
		user_to = ''
		user_date = ''
		user_month = ''
		user_year = ''
		user_time = ''
		user_comments = ''
		user_status = 'отменен'
		indices = 0

		for ind in requests.index:
			if ((requests['chat_id'][ind]==user_chat_id) and pd.isnull(requests['status'][ind])):
				indices = ind
				user_message_id = requests['message_id'][ind]
				user_from = requests['from'][ind]
				user_to = requests['to'][ind]
				user_date = str(requests['day'][ind])
				user_month = str(requests['month'][ind])
				user_year = str(requests['year'][ind])
				user_time = requests['time'][ind]
				user_comments = requests['comment'][ind]
		if(str(message.text)==str(user_message_id)):
			bot.delete_message(otyrartaxi_id, int(message.text))
			bot.send_message(message.chat.id, 'Ваш заказ остановлен!')
			requests = requests.drop([indices])
			request = pd.DataFrame({"chat_id":[user_chat_id], 
								"message_id":[user_message_id],
								"from":[user_from],
								"to":[user_to],
								"day":[user_date],
								"month":[user_month],
								"year":[user_year],
								"time":[user_time],
								"comment":[user_comments],
								"status":[user_status]})
			requests = requests.append(request, ignore_index=True)
			#writing to scv file
			requests.to_csv(r'drivers_requests.csv', index = False, header=True, encoding='cp1251')

			#deleting from resending_req_user.csv
			rtu = pd.read_csv('resending_req_user.csv', sep=',', encoding='cp1251')
			rtus = rtu[rtu['group_message_id']==user_message_id]
			if(rtus.empty==False):
				user_id = rtus['user_id'].values
				user_id = int(user_id[0])
				message_id = rtus['to_user_message_id'].values
				message_id = int(message_id[0])
				bot.delete_message(user_id, message_id)
				indices = 0
				rtu = rtu[rtu['group_message_id']!=int(user_message_id)]
				rtu.to_csv(r'resending_req_user.csv', index = False, header=True, encoding='cp1251')

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "Можете совершать услуги", reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
		else:
			msg = bot.send_message(message.chat.id, "Код подтверждения не правильный")
			bot.register_next_step_handler(msg, process_driver_req_canceling_accept)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('Добавить заявку➕')
		itembtn2 = types.KeyboardButton('Статистика📈')
		itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
		markup.add(itembtn1, itembtn2, itembtn3)
		msg = bot.send_message(message.chat.id, "Извините, ошибка.\nЗаполните заново!", reply_markup = markup)
#---------------END-CANCELING---------------------------------------------------------------------------------------------------------------------


#Statistic for driver
def get_statistic(message):
	try:
		user_id = int('{0.id}'.format(message.from_user, bot.get_me()))
		if(message.text == 'Активность по времени'):
			ax = 0
			requests = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
			requests = requests[requests['chat_id']==user_id]
			requests = requests.groupby(['time'], as_index=False).count()
			requests.chat_id = requests.chat_id.astype(int)
			ax = sns.catplot(x='time', y='chat_id', kind='bar', data=requests, palette='deep').set(title='Активность по времени', xlabel='Время', ylabel='Количесвто')
			plt.xticks(rotation=60)
			ax.savefig("figure.png", dpi=300)
			photo = open("figure.png", 'rb')
			bot.send_photo(message.chat.id, photo)
			photo.close()
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "Совершайте услуги, я вам только рад🙃", reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
		elif(message.text == 'Активность по городам'):
			ax = 0
			requests = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
			requestsA = requests.groupby(['from'], as_index=False).count()
			requestsB = requests.groupby(['to'], as_index=False).count()
			ax = sns.catplot(x='from', y='chat_id', kind='bar', data=requestsA, palette='deep').set(title='Активность по городам(точки А)', xlabel='Город', ylabel='Количесвто')
			ax.savefig("figure.png", dpi=300)
			photo = open("figure.png", 'rb')
			bot.send_photo(message.chat.id, photo)
			photo.close()
			ax = 0
			ax = sns.catplot(x='to', y='chat_id', kind='bar', data=requestsB, palette='deep').set(title='Активность по городам(точки B)', xlabel='Город', ylabel='Количесвто')
			ax.savefig("figure.png", dpi=300)
			photo = open("figure.png", 'rb')
			bot.send_photo(message.chat.id, photo)
			photo.close()
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "Совершайте услуги, я вам только рад🙃", reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
		elif(message.text == 'Активность по дням недели'):
			ax = 0
			mon = 0
			tue = 0
			wed = 0
			thu = 0
			fri = 0
			sat = 0
			sun = 0
			requests = pd.read_csv('users_requests.csv', sep=',', encoding='cp1251')
			for ind in requests.index:
				weekdate = date(int(requests['year'][ind]),int(requests['month'][ind]),int(requests['day'][ind]))
				weekday = weekdate.weekday()
				if(int(weekday)==1):
					mon+=1
				elif(int(weekday)==2):
					tue+=1
				elif(int(weekday)==3):
					wed+=1
				elif(int(weekday)==4):
					thu+=1
				elif(int(weekday)==5):
					fri+=1
				elif(int(weekday)==6):
					sat+=1
				elif(int(weekday)==7):
					sun+=1

			data = {'weekdays':['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'], 
					'quantity':[mon, tue, wed, thu, fri, sat, sun]} 
			# Create DataFrame 
			df = pd.DataFrame(data)
			ax = sns.catplot(x='weekdays', y='quantity', kind='bar', data=df, palette='deep').set(title='Активность по дням недели', xlabel='День недели', ylabel='Количесвто')
			plt.xticks(rotation=30)
			ax.savefig("figure.png", dpi=300)
			photo = open("figure.png", 'rb')
			bot.send_photo(message.chat.id, photo)
			photo.close()

			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "Совершайте услуги, я вам только рад🙃", reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
		elif(message.text == '🔙Назад'):
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Добавить заявку➕')
			itembtn2 = types.KeyboardButton('Статистика📈')
			itembtn3 = types.KeyboardButton('Стать Пассажиром👤')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, "Совершайте услуги, я вам только рад🙃", reply_markup = markup)
			bot.register_next_step_handler(msg, chosing_diver)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('Моя статистика')
			itembtn2 = types.KeyboardButton('Активность водителей')
			itembtn3 = types.KeyboardButton('Активность по городам')
			itembtn4 = types.KeyboardButton('🔙Назад')

			markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

			msg = bot.send_message(message.chat.id, 'Не понял :(', reply_markup=markup)
			bot.register_next_step_handler(msg, get_statistic)
	except Exception as e:
		bot.reply_to(message, 'Ошибка\nERROR: Статистика📈 get_statistic!')

# RUN
bot.polling(none_stop=True)