import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config

bot = telebot.TeleBot("my_api")

@bot.message_handler(commands = ['start'])
def hi(message):
	bot.send_message(message.chat.id, 'Добро пожаловать в Weather Bot, ' + str(message.from_user.first_name) +
                     "! Чтобы узнать команды бота, напишите */help* или нажмите на подсвеченное слово")

@bot.message_handler(commands = ['help'])
def help(message):
	bot.send_message(message.chat.id, 'Список команд:' + '\n' + "/help - список команд" + '\n' +
                     "/credits - разработчик бота" + '\n' + "/weather - узнать погоду в населённом пункте")

@bot.message_handler(commands = ['weather'])
def weather(message):
    bot.send_message(message.chat.id, "Теперь напишите название населённого пункта!")
    @bot.message_handler(content_types = ['text'])
    def weather(message):
        try:
            place = message.text

            config_dict = get_default_config()
            config_dict['language'] = 'ru'

            owm = OWM('my_api', config_dict)
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(place)
            weat = observation.weather

            t = weat.temperature("celsius")
            cur_t = t['temp']
            feel_t = t['feels_like']
            max_t= t['temp_max']
            min_t = t['temp_min']

            wind = weat.wind()['speed']
            humid = weat.humidity
            dt = weat.detailed_status
            davl = weat.pressure['press']

            bot.send_message(message.chat.id, "В городе " + str(place) + ":" + '\n' + "Температура: " + str(cur_t) + " °C" + "\n" +
                    "Максимальная температура в течение суток: " + str(max_t) + " °C" +"\n" +
                    "Минимальная температура в течение суток: " + str(min_t) + " °C" + "\n" +
                    "Ощущается как: " + str(feel_t) + " °C" + "\n" +
                    "Скорость ветра равна " + str(wind) + " м/с" + "\n" +
                    "Давление: " + str(davl) + " мм.рт.ст" + "\n" +
                    "Влажность: " + str(humid) + " %" + "\n" + str(dt))
            bot.send_message(message.chat.id, "Спасибо, что пользуетесь Weather Bot, можете отправить свой отзыв о боте разработчику(@aizerg)")
        except:
            bot.send_message(message.chat.id, "Такой город не найден!" + " Проверьте правильность написания названия города." +
                             " В случае, если Вы уверены, что название написано правильно, напишите разработчику в Telegram: @aizerg")


@bot.message_handler(commands = ['credits'])
def credits(message):
    bot.send_message(message.chat.id, "Разработчик: @aizerg" + '\n\n' + "Буду не против отзывов :)")


bot.polling(none_stop = True, interval = 0)
