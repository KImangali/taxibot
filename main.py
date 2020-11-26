import telebot
import datetime
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, "ru") 

from telebot import types

current_datetime = datetime.now()

token = '1416332736:AAFS-quEAN1WDRzBcCWhJGi1wAP4q4Efl5c'
bot = telebot.TeleBot(token)
otyrartaxi_id = "@otyrartaxi"

user_dict = {}

class User:
    def __init__(self, fullname):
        self.fullname = fullname

        keys = ['fullname', 'phone', 'A', 
                'B', 'date', 'hour', 'minute']
        
        for key in keys:
            self.key = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
	sti = open('static/sticker.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
	itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
	markup.add(itembtn1)

	msg = bot.send_message(message.chat.id, "Salem, {0.first_name}!\n Men - <b>{1.first_name}</b>, taksi servisimin. Tapsiris beru ushun astindagi Batirmani bas".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup = markup)
	

@bot.message_handler(commands=['Jana_Tapsiris'])
def process_name(message):
	try:
		#удалить старую клавиатуру
		markup = types.ReplyKeyboardRemove(selective=False)

		msg = bot.send_message(message.chat.id, 'Esiminiz:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_phone)
	except Exception as e:
		bot.reply_to(message, 'Name duris emes!')

def process_phone(message):
	try:
		user_dict[message.chat.id] = User(message.text)

		msg = bot.send_message(message.chat.id, 'Nomeriniz:\n Misal: 87771234656')
		bot.register_next_step_handler(msg, process_from)
	except Exception as e:
		bot.reply_to(message, 'Nomeriniz duris emes!')

def process_from(message):
	try:
		user = user_dict[message.chat.id]
		if len(message.text) != 11:
			bot.send_message(message.chat.id, 'For Error', reply_markup=err)
		if message.text[0] != '8':
			bot.send_message(message.chat.id, 'For Error', reply_markup=err)
		if message.text[1]!='7':
			bot.send_message(message.chat.id, 'For Error', reply_markup=err)

		user.phone = int(message.text)

		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Shauldir')
		itembtn2 = types.KeyboardButton('Shymkent')
		itembtn3 = types.KeyboardButton('Turkestan')
		markup.add(itembtn1, itembtn2, itembtn3)

		msg = bot.send_message(message.chat.id, 'Kaidan shigasiz(A)?', reply_markup=markup)
		bot.register_next_step_handler(msg, process_to)
	except Exception as e:
		msg = bot.reply_to(message, 'Nomeriniz duris emes, basinan zhaz! \n Misal: 87771234656')
		bot.register_next_step_handler(msg, process_from)

def process_to(message):
	try:
		if message.text=='Shauldir' or message.text=='Shymkent' or message.text=='Turkestan':
			user = user_dict[message.chat.id]
			user.A = message.text
			
			if message.text == "Shauldir":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shymkent')
				itembtn2 = types.KeyboardButton('Turkestan')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'Kaida barasiz(B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif message.text == "Shymkent":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shauldir')
				itembtn2 = types.KeyboardButton('Turkestan')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'Kaida barasiz(B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif message.text == "Turkestan":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shauldir')
				itembtn2 = types.KeyboardButton('Shymkent')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'Kaida barasiz(B)?', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Shauldir')
			itembtn2 = types.KeyboardButton('Shymkent')
			itembtn3 = types.KeyboardButton('Turkestan')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, 'Tek astinda korsetilgen mekendi tandaniz!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to)
		
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)

def process_date(message):
	try:
		if message.text=='Shauldir' or message.text=='Shymkent' or message.text=='Turkestan':
			user = user_dict[message.chat.id]
			user.B = message.text

			time_diff1 = timedelta(days=1)
			time_diff2 = timedelta(days=2)
			time_diff3 = timedelta(days=3)
			time_diff4 = timedelta(days=4)
			time_diff5 = timedelta(days=5)

			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton(str(current_datetime.day) + ' ' + str(current_datetime.strftime("%A")))
			itembtn2 = types.KeyboardButton(str((current_datetime + time_diff1).day) + ' ' + (current_datetime + time_diff1).strftime("%A"))
			itembtn3 = types.KeyboardButton(str((current_datetime + time_diff2).day) + ' ' + (current_datetime + time_diff2).strftime("%A"))
			itembtn4 = types.KeyboardButton(str((current_datetime + time_diff3).day) + ' ' + (current_datetime + time_diff3).strftime("%A"))
			itembtn5 = types.KeyboardButton(str((current_datetime + time_diff4).day) + ' ' + (current_datetime + time_diff4).strftime("%A"))
			itembtn6 = types.KeyboardButton(str((current_datetime + time_diff5).day) + ' ' + (current_datetime + time_diff5).strftime("%A"))

			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

			msg = bot.send_message(message.chat.id, 'Kun:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time_hour)
		else:
			user = user_dict[message.chat.id]
			if user.A=="Shauldir":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shymkent')
				itembtn2 = types.KeyboardButton('Turkestan')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'Tek astinda korsetilgen mekendi tandaniz!')
				bot.register_next_step_handler(msg, process_date)
			elif user.A=="Shymkent":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shauldir')
				itembtn2 = types.KeyboardButton('Turkestan')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'Tek astinda korsetilgen mekendi tandaniz!')
				bot.register_next_step_handler(msg, process_date)
			elif user.A=="Turkestan":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shauldir')
				itembtn2 = types.KeyboardButton('Shymkent')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'Tek astinda korsetilgen mekendi tandaniz!')
				bot.register_next_step_handler(msg, process_date)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)
		
def process_time_hour(message):
	try:
		user = user_dict[message.chat.id]
		user.date = message.text

		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('01')
		itembtn2 = types.KeyboardButton('02')
		itembtn3 = types.KeyboardButton('03')
		itembtn4 = types.KeyboardButton('04')
		itembtn5 = types.KeyboardButton('05')
		itembtn6 = types.KeyboardButton('06')
		itembtn7 = types.KeyboardButton('07')
		itembtn8 = types.KeyboardButton('08')
		itembtn9 = types.KeyboardButton('09')
		itembtn10 = types.KeyboardButton('10')
		itembtn11 = types.KeyboardButton('11')
		itembtn12 = types.KeyboardButton('12')
		itembtn13 = types.KeyboardButton('13')
		itembtn14 = types.KeyboardButton('14')
		itembtn15 = types.KeyboardButton('15')
		itembtn16 = types.KeyboardButton('16')
		itembtn17 = types.KeyboardButton('17')
		itembtn18 = types.KeyboardButton('18')
		itembtn19 = types.KeyboardButton('19')
		itembtn20 = types.KeyboardButton('20')
		itembtn21 = types.KeyboardButton('21')
		itembtn22 = types.KeyboardButton('22')
		itembtn23 = types.KeyboardButton('23')
		itembtn24 = types.KeyboardButton('24')

		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12, itembtn13, itembtn14, itembtn15, itembtn16, itembtn17, itembtn18, itembtn19, itembtn20, itembtn21, itembtn22, itembtn23, itembtn24)

		msg = bot.send_message(message.chat.id, 'Sagat:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_time_minute)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)
def process_time_minute(message):
	try:
		user = user_dict[message.chat.id]
		user.hour = message.text

		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('00')
		itembtn2 = types.KeyboardButton('10')
		itembtn3 = types.KeyboardButton('20')
		itembtn4 = types.KeyboardButton('30')
		itembtn5 = types.KeyboardButton('40')
		itembtn6 = types.KeyboardButton('50')

		markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

		msg = bot.send_message(message.chat.id, 'Minut:', reply_markup=markup)
		bot.register_next_step_handler(msg, process_prefinishing)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)
def process_prefinishing(message):
	try:
		user = user_dict[message.chat.id]
		user.minute = message.text

		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
		itembtn1 = types.KeyboardButton('Aiaktau')
		itembtn2 = types.KeyboardButton('Ozgertu')
		itembtn3 = types.KeyboardButton('Toktatu')

		markup.add(itembtn1, itembtn2, itembtn3)

		last_text = '<i><b>' + user.fullname + '</b></i>, sizdin tapsirisiniz: \n 📞: <i><b>' + str(user.phone) + '</b></i>\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.date + '</b></i>\n 🕐: <i><b>' + str(user.hour) + ':' + str(user.minute) + '</b></i>'

		msg = bot.send_message(message.chat.id, last_text, reply_markup=markup, parse_mode='html') 
		bot.register_next_step_handler(msg, process_finishing)


	except Exception as e:
		bmarkup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)
def process_finishing(message):
	try:
		user = user_dict[message.chat.id]
		if message.text=='Aiaktau':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Tapsiristi toktatu')
			
			markup.add(itembtn1)
			
			last_text = '👤:  <a href="tg://user?id={0.id}">' + user.fullname + '</a> \n 📞: ' + str(user.phone) + '\n A:  <i><b>' + user.A + '</b></i>\n B:  <i><b>' + user.B + '</b></i>\n 📅: <i><b>' + user.date + '</b></i>\n 🕐: <i><b>' + str(user.hour) + ':' + str(user.minute) + '</b></i>'
			
			msg = bot.send_message(otyrartaxi_id, last_text.format(message.from_user, bot.get_me()), parse_mode='html')
			msg = bot.send_message(message.chat.id, 'Sizdin tapsirisiniz kosildi! Kutiniz...\n Tapsiristi toktatu kodi: ' + str(msg.id), reply_markup=markup)
			bot.register_next_step_handler(msg, process_canceling)
		elif message.text=='Ozgertu':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Esim')
			itembtn2 = types.KeyboardButton('Telephon')
			itembtn3 = types.KeyboardButton('A')
			itembtn4 = types.KeyboardButton('B')
			itembtn5 = types.KeyboardButton('Kun')
			itembtn6 = types.KeyboardButton('Uakit')
			itembtn7 = types.KeyboardButton('ARTKA')
			
			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7)
			
			msg = bot.send_message(message.chat.id, 'Ozgertetin kezde malimetterdi kelgen zhrinen zhalgastirasiz!\n Kandai malimetti ozgertesiz?', reply_markup=markup)
			bot.register_next_step_handler(msg, process_editing)
		else:
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
			itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
			markup.add(itembtn1)
			
			msg = bot.send_message(message.chat.id, "{0.username} tapsiris beru ushun /Jana_Tapsiris basiniz".format(message.from_user, bot.get_me()), reply_markup = markup)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)

def process_editing(message):
	try:
		if message.text=='Esim':
			msg = bot.send_message(message.chat.id, 'Ozgertudi bastaniz.')
			bot.register_next_step_handler(msg, process_phone)
		elif message.text=='Telephon':
			msg = bot.reply_to(message, 'Nomerinizdi engiziniz! \n Misal: 87771234656')
			bot.register_next_step_handler(msg, process_from)
		elif message.text=='A':
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Shauldir')
			itembtn2 = types.KeyboardButton('Shymkent')
			itembtn3 = types.KeyboardButton('Turkestan')
			markup.add(itembtn1, itembtn2, itembtn3)
			msg = bot.send_message(message.chat.id, 'A punktin tandaniz!', reply_markup=markup)
			bot.register_next_step_handler(msg, process_to)
		elif message.text=='B':
			user = user_dict[message.chat.id]
			if user.A=="Shauldir":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shymkent')
				itembtn2 = types.KeyboardButton('Turkestan')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'B punktin tandaniz!', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif user.A=="Shymkent":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shauldir')
				itembtn2 = types.KeyboardButton('Turkestan')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'B punktin tandaniz!', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
			elif user.A=="Turkestan":
				markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
				itembtn1 = types.KeyboardButton('Shauldir')
				itembtn2 = types.KeyboardButton('Shymkent')
				markup.add(itembtn1, itembtn2)
				msg = bot.send_message(message.chat.id, 'B punktin tandaniz!', reply_markup=markup)
				bot.register_next_step_handler(msg, process_date)
		elif message.text=='Kun':
			user = user_dict[message.chat.id]
			time_diff1 = timedelta(days=1)
			time_diff2 = timedelta(days=2)
			time_diff3 = timedelta(days=3)
			time_diff4 = timedelta(days=4)
			time_diff5 = timedelta(days=5)

			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton(str(current_datetime.day) + ' ' + str(current_datetime.strftime("%A")))
			itembtn2 = types.KeyboardButton(str((current_datetime + time_diff1).day) + ' ' + (current_datetime + time_diff1).strftime("%A"))
			itembtn3 = types.KeyboardButton(str((current_datetime + time_diff2).day) + ' ' + (current_datetime + time_diff2).strftime("%A"))
			itembtn4 = types.KeyboardButton(str((current_datetime + time_diff3).day) + ' ' + (current_datetime + time_diff3).strftime("%A"))
			itembtn5 = types.KeyboardButton(str((current_datetime + time_diff4).day) + ' ' + (current_datetime + time_diff4).strftime("%A"))
			itembtn6 = types.KeyboardButton(str((current_datetime + time_diff5).day) + ' ' + (current_datetime + time_diff5).strftime("%A"))

			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

			msg = bot.send_message(message.chat.id, 'Kundi tandaniz:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time_hour)
		elif message.text=='Uakit':
			user = user_dict[message.chat.id]

			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('01')
			itembtn2 = types.KeyboardButton('02')
			itembtn3 = types.KeyboardButton('03')
			itembtn4 = types.KeyboardButton('04')
			itembtn5 = types.KeyboardButton('05')
			itembtn6 = types.KeyboardButton('06')
			itembtn7 = types.KeyboardButton('07')
			itembtn8 = types.KeyboardButton('08')
			itembtn9 = types.KeyboardButton('09')
			itembtn10 = types.KeyboardButton('10')
			itembtn11 = types.KeyboardButton('11')
			itembtn12 = types.KeyboardButton('12')
			itembtn13 = types.KeyboardButton('13')
			itembtn14 = types.KeyboardButton('14')
			itembtn15 = types.KeyboardButton('15')
			itembtn16 = types.KeyboardButton('16')
			itembtn17 = types.KeyboardButton('17')
			itembtn18 = types.KeyboardButton('18')
			itembtn19 = types.KeyboardButton('19')
			itembtn20 = types.KeyboardButton('20')
			itembtn21 = types.KeyboardButton('21')
			itembtn22 = types.KeyboardButton('22')
			itembtn23 = types.KeyboardButton('23')
			itembtn24 = types.KeyboardButton('24')

			markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11, itembtn12, itembtn13, itembtn14, itembtn15, itembtn16, itembtn17, itembtn18, itembtn19, itembtn20, itembtn21, itembtn22, itembtn23, itembtn24)

			msg = bot.send_message(message.chat.id, 'Sagat:', reply_markup=markup)
			bot.register_next_step_handler(msg, process_time_minute)
		else:
			markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
			itembtn1 = types.KeyboardButton('Aiaktau')
			itembtn2 = types.KeyboardButton('Ozgertu')
			itembtn3 = types.KeyboardButton('Toktatu')

			markup.add(itembtn1, itembtn2, itembtn3)


			msg = bot.send_message(message.chat.id, 'Tapsiristi Aiaktau/Ozgertu/Toktatu', reply_markup=markup) 
			bot.register_next_step_handler(msg, process_finishing)
	except Exception as e:
		bot.reply_to(message, 'Canceling duris emes!')

def process_canceling(message):
	try:
		if message.text=='Tapsiristi toktatu':
			msg = bot.send_message(message.chat.id, 'Tapsiristi tokatatu kodin zhbernz: ')
			bot.register_next_step_handler(msg, process_canceling_accept)
		else:
			msg = bot.send_message(message.chat.id, 'Sizdin tapsirisiniz ayaktalgan zhok!')
			bot.register_next_step_handler(msg, process_canceling)
	except Exception as e:
		bot.reply_to(message, 'Canceling duris emes!')
def process_canceling_accept(message):
	try:
		bot.delete_message(otyrartaxi_id, int(message.text))
		bot.send_message(message.chat.id, 'Sizdin tapsirisiniz toktatildi!')

		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "{0.username} tapsiris beru ushun /Jana_Tapsiris basiniz".format(message.from_user, bot.get_me()), reply_markup = markup)
	except Exception as e:
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
		itembtn1 = types.KeyboardButton('/Jana_Tapsiris')
		markup.add(itembtn1)

		msg = bot.send_message(message.chat.id, "Keshiriniz, bir kate boldi.\nBasinan toltyruynizdi suraymiz", reply_markup = markup)


# RUN
bot.polling(none_stop=True)