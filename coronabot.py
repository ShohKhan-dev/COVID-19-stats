import telebot
import time
from telebot import types
import requests
import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
import sqlite3
from pytz import timezone

#conn=sqlite3.connect('CoronaData.db')
#conn.execute("CREATE TABLE CORONA (Country, Virus, New_virus, Dead, New_dead, Recovered, Now_virus, Hard, Checked, Qit)")
#conn.execute("CREATE TABLE TIMER (Day, Nowtime)")
#conn.execute("CREATE TABLE TIMER2 (Day, Nowtime)")
#conn.close()

user_dict = {}

class User:
    def __init__(self, qiymat, array):
        self.qiymat = qiymat
        self.array = array

#bot = telebot.TeleBot(token = '1246668421:AAFduvP_U5ni-K4uC7X0V1tn4sJ5BJZ-KRo')
bot = telebot.TeleBot(token = '833733976:AAE92wcBdR7snpqiqsHSkSuv9Ly0XLvWehM')

@bot.message_handler(commands=['start'])

def starting(message):
    name = str(message.from_user.first_name)
    bot.reply_to(message, 'Assalomu alaykum ' + name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    total_data = types.KeyboardButton("Umumiy ma'lumot")
    small_data = types.KeyboardButton("Davlatlar bo'yicha ma'lumot")
    help_info = types.KeyboardButton("Yordam\Ko'rsatma")
    
    markup.add(total_data,small_data)
    markup.add(help_info)
    bot.send_message(message.chat.id,'''
    Bu bot Dunyo bo'ylab Koronavirusdan zararlanganlar soni haqida ma'lumot beradi!
    ''',reply_markup=markup,parse_mode='markdown')



def totaldata():
    URL = 'https://kun.uz'
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find('div', class_ = 'covid-block__list')

    ozbekiston = []
    dunyo = []

    for item in results:
        for bola in item:
            for i in bola:
                for k in i:
                    for x in k:
                        if x.isdigit():
                            ozbekiston.append(x)
                            
    #### SECoND ONE, WORLDS STATUS

    req = Request("https://www.worldometers.info/coronavirus", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup2 = BeautifulSoup(webpage, 'html.parser')
    virused = soup2.find_all('div', class_ = 'maincounter-number')

    for item in virused:
        for person in item:
            for that in person:
                if that != '\n':
                    dunyo.append(that)
                
    here = []
    there = []

    here.append("Virus yuqtirganlar:  " + str(ozbekiston[0]))
    here.append("Sog'ayganlar:  " + str(ozbekiston[1]))
    here.append("Vafot etganlar:  " + str(ozbekiston[2]))

    there.append("Virus yuqtirganlar:  " + str(dunyo[0]))
    there.append("Sog'ayganlar:  " + str(dunyo[2]))
    there.append("Vafot etganlar:  " + str(dunyo[1]))
    
    uzbeks = '\n'.join(here)
    alls = '\n'.join(there)

    conner = sqlite3.connect('CoronaData.db')
    
    conner.execute("DELETE FROM TIMER2")

    day = datetime.now(timezone('Asia/Tashkent')).strftime('%d')
    hour = datetime.now(timezone('Asia/Tashkent')).strftime('%H')
    minute = datetime.now(timezone('Asia/Tashkent')).strftime('%M')
    time  = int(hour)*60 + int(minute)

    conner.execute("INSERT INTO TIMER2 (Day, Nowtime) VALUES (?, ?)", (day, time))
    conner.commit()
    conner.close()
    
    file = open("Totaldata.txt", "w")
    
    answer = "O'ZBEKISTON HUDUDIDA:" + '\n' + uzbeks + '\n\n' + "DUNYO BO'YLAB:" + '\n' + alls
    
    file.write(answer)
    file.close()

    return answer

def main_data():
    
    data = []

    req = Request("https://www.worldometers.info/coronavirus", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    soup2 = BeautifulSoup(webpage, 'html.parser')

    result = soup2.find('table', id = 'main_table_countries_today')

    table = result.find('tbody')

    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols])

    
    ### FILTERING
    
    for _ in range(8):
        data.pop(0)

    for item in data:
        item.pop(11)
        item.pop(9)
        item.pop(8)

    ### Translating data

    tarjima = {'Afghanistan': "Afg'oniston", 'Albania': 'Albaniya', 'Algeria': 'Jazoir',
               'Andorra': 'Andorra', 'Angola': 'Angola', 'Anguilla': 'Anguilla',
               'Antigua and Barbuda': 'Antigua va Barbuda', 'Argentina': 'Argentina',
               'Armenia': 'Armaniston', 'Aruba': 'Aruba', 'Australia': 'Avstraliya',
               'Austria': 'Avstriya', 'Azerbaijan': 'Ozarbayjon', 'Bahamas': 'Bagama orollari',
               'Bahrain': 'Bahrayn', 'Bangladesh': 'Bangladesh', 'Barbados': 'Barbados',
               'Belarus': 'Belarus', 'Belgium': 'Belgiya', 'Belize': 'Beliz', 'Benin': 'Benin',
               'Bermuda': 'Bermuda', 'Bhutan': 'Butan', 'Bolivia': 'Boliviya',
               'Bosnia and Herzegovina': 'Bosniya va Gertsegovina', 'Botswana': 'Botsvana',
               'Brazil': 'Braziliya', 'British Virgin Islands': 'Britaniya Virgin orollari',
               'Brunei': 'Bruney', 'Bulgaria': 'Bolgariya', 'Burkina Faso': 'Burkina Faso',
               'Burundi': 'Burundi', 'CAR': 'CAR', 'Cabo Verde': 'Cabo Verde', 'Cambodia': 'Kambodja',
               'Cameroon': 'Kamerun', 'Canada': 'Kanada', 'Caribbean Netherlands': 'Caribbean Niderlandiya',
               'Cayman Islands': 'Kayman orollari', 'Chad': 'Chad', 'Channel Islands': 'Channel orollari',
               'Chile': 'Chili', 'China': 'Xitoy', 'Colombia': 'Kolumbiya', 'Congo': 'Kongo', 'Costa Rica': 'Kosta-Rika',
               'Croatia': 'Xorvatiya', 'Cuba': 'Kuba', 'Curaçao': 'Curaçao', 'Cyprus': 'Kipr', 'Czechia': 'Chexiya',
               'DRC': 'DRC', 'Denmark': 'Daniya', 'Diamond Princess': 'Diamond Princess', 'Djibouti': 'Jibuti', 'Dominica': 'Dominika',
               'Dominican Republic': 'Dominik Respublikasi', 'Ecuador': 'Ekvador', 'Egypt': 'Misr', 'El Salvador': 'El Salvador',
               'Equatorial Guinea': 'Ekvatorial Gvineya', 'Eritrea': 'Eritreya', 'Estonia': 'Estoniya', 'Eswatini': 'Eswatini',
               'Ethiopia': 'Efiopiya', 'Faeroe Islands': 'Farer orollari', 'Falkland Islands': 'Folklend orollari', 'Fiji': 'Fiji',
               'Finland': 'Finlyandiya', 'France': 'Frantsiya', 'French Guiana': 'Fransuz Gvianasi', 'French Polynesia': 'Fransuz Polineziyasi',
               'Gabon': 'Gabon', 'Gambia': 'Gambiya', 'Georgia': 'Gruziya', 'Germany': 'Germaniya', 'Ghana': 'Gana', 'Gibraltar': 'Gibraltar',
               'Greece': 'Gretsiya', 'Greenland': 'Grenlandiya', 'Grenada': 'Grenada', 'Guadeloupe': 'Guadeloupe', 'Guatemala': 'Gvatemala',
               'Guinea': 'Gvineya', 'Guinea-Bissau': 'Gvineya-Bissau', 'Guyana': 'Gayana', 'Haiti': 'Gaiti', 'Honduras': 'Gonduras',
               'Hong Kong': 'Gonkong', 'Hungary': 'Vengriya', 'Iceland': 'Islandiya', 'India': 'Hindiston', 'Indonesia': 'Indoneziya',
               'Iran': 'Eron', 'Iraq': 'Iroq', 'Ireland': 'Irlandiya', 'Isle of Man': 'Jurnal of Man', 'Israel': 'Isroil',
               'Italy': 'Italiya', 'Ivory Coast': "Kot-d'Ivuar", 'Jamaica': 'Yamayka', 'Japan': 'Yaponiya', 'Jordan': 'Jordan',
               'Kazakhstan': "Qozog'iston", 'Kenya': 'Keniya', 'Kuwait': 'Kuvayt', 'Kyrgyzstan': "Qirg'iziston", 'Laos': 'Laos',
               'Latvia': 'Latviya', 'Lebanon': 'Livan', 'Liberia': 'Liberiya', 'Libya': 'Liviya', 'Liechtenstein': 'Lixtenshteyn',
               'Lithuania': 'Litva', 'Luxembourg': 'Lyuksemburg', 'MS Zaandam': 'MS Zaandam', 'Macao': 'Makao', 'Madagascar': 'Madagaskar',
               'Malawi': 'Malavi', 'Malaysia': 'Malayziya', 'Maldives': 'Maldiv orollari', 'Mali': 'Mali', 'Malta': 'Malta', 'Martinique': 'Martinika',
               'Mauritania': 'Mavritaniya', 'Mauritius': 'Mavrikiy', 'Mayotte': 'Mayotte', 'Mexico': 'Meksika', 'Moldova': 'Moldova', 'Monaco': 'Monako',
               'Mongolia': "Mo'g'uliston", 'Montenegro': 'Chernogoriya', 'Montserrat': 'Montserrat', 'Morocco': 'Marokash', 'Mozambique': 'Mozambik',
               'Myanmar': 'Myanma', 'Namibia': 'Namibiya', 'Nepal': 'Nepal', 'Netherlands': 'Niderlandiya', 'New Caledonia': 'Yangi Kaledoniya',
               'New Zealand': 'Yangi Zelandiya', 'Nicaragua': 'Nikaragua', 'Niger': 'Niger', 'Nigeria': 'Nigeriya', 'North Macedonia': 'Shimoliy Makedoniya',
               'Norway': 'Norvegiya', 'Oman': 'Ummon', 'Pakistan': 'Pokiston', 'Palestine': 'Falastin', 'Panama': 'Panama', 'Papua New Guinea': 'Papua Yangi Gvineya',
               'Paraguay': 'Paragvay', 'Peru': 'Peru', 'Philippines': 'Filippin', 'Poland': 'Polsha', 'Portugal': 'Portugaliya', 'Qatar': 'Qatar', 'Romania': 'Ruminiya',
               'Russia': 'Rossiya', 'Rwanda': 'Ruanda', 'Réunion': 'Réunion', 'S. Korea': 'Janubiy Koreya', 'Saint Kitts and Nevis': 'Sent-Kits va Nevis',
               'Saint Lucia': 'Saint Lucia', 'Saint Martin': 'Sankt Martin', 'Saint Pierre Miquelon': 'Sankt-Per Miquelon', 'San Marino': 'San Marino',
               'Sao Tome and Principe': 'San Tome va Prinsipi', 'Saudi Arabia': 'Saudiya Arabistoni', 'Senegal': 'Senegal', 'Serbia': 'Serbiya',
               'Seychelles': 'Seyshel orollari', 'Sierra Leone': 'Syerra-Leone', 'Singapore': 'Singapur', 'Sint Maarten': 'Sint Taiti', 'Slovakia': 'Slovakiya',
               'Slovenia': 'Sloveniya', 'Somalia': 'Somali', 'South Africa': 'Janubiy Afrika', 'South Sudan': 'Janubiy Sudan', 'Spain': 'Ispaniya',
               'Sri Lanka': 'Shri Lanka', 'St. Barth': 'Sankt Barth', 'St. Vincent Grenadines': 'Sankt-Vinsent Grenadin', 'Sudan': 'Sudan', 'Suriname': 'Surinam',
               'Sweden': 'Shvetsiya', 'Switzerland': 'Shveytsariya', 'Syria': 'Suriya', 'Taiwan': 'Tayvan', 'Tanzania': 'Tanzaniya', 'Thailand': 'Tailand',
               'Timor-Leste': 'Timor-Leste', 'Togo': 'Togo', 'Trinidad and Tobago': 'Trinidad va Tobago', 'Tunisia': 'Tunis', 'Turkey': 'Turkiya',
               'Turks and Caicos': 'Turk va Kaykos',
               'UAE': 'BAA', 'UK': 'Buyuk Britaniya', 'USA': 'AQSH', 'Uganda': 'Uganda', 'Ukraine': 'Ukraina', 'Uruguay': 'Urugvay',
               'Uzbekistan': "O'zbekiston", 'Vatican City': 'Vatikan', 'Venezuela': 'Venesuela', 'Vietnam': 'Vetnam',
               'Western Sahara': 'Western Sahara', 'Yemen': 'Yaman', 'Zambia': 'Zambiya', 'Zimbabwe': 'Zimbabve'}
    qitas = {'Asia' : 'Osiyo', 'Europe' : 'Yevropa', 'North America' : 'Shimoliy America', 'South America': 'Janubiy America', 'Africa' : 'Afrika', 'Australia/Oceania' : 'Avstraliya'}
    
    
    for tar in data:
        if tar[0] in tarjima:
            tar[0] = tarjima[tar[0]]
        if tar[-1] in qitas:
            tar[-1] = qitas[tar[-1]]
            
    conn=sqlite3.connect('CoronaData.db')
            
    conn.execute("DELETE FROM CORONA")

    conn.execute("DELETE FROM TIMER")


    day = datetime.now(timezone('Asia/Tashkent')).strftime('%d')
    hour = datetime.now(timezone('Asia/Tashkent')).strftime('%H')
    minute = datetime.now(timezone('Asia/Tashkent')).strftime('%M')

    time  = int(hour)*60 + int(minute)



    for item in data:
        conn.execute("INSERT INTO CORONA (Country, Virus, New_virus, Dead, New_dead, Recovered, Now_virus, Hard, Checked, Qit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                     (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]))

    conn.execute("INSERT INTO TIMER (Day, Nowtime) VALUES (?, ?)", (day, time))


    conn.commit()

    conn.close()


    return data

            


@bot.message_handler(content_types=['text'], func = lambda message: message.text == "Umumiy ma'lumot")

def total(message):
    dtime = datetime.now(timezone('Asia/Tashkent')).strftime("Sana: %d-%m-%Y yil \nSoat: %H:%M dagi holat bo'yicha: ")
    
    con = sqlite3.connect('CoronaData.db')

    day = [days for days in con.execute("SELECT Day FROM TIMER2")]
    last_time = [times for times in con.execute("SELECT Nowtime FROM TIMER2")]

    day = int(day[0][0])
    last_time = int(last_time[0][0])

    today = int(datetime.now(timezone('Asia/Tashkent')).strftime("%d"))
    now_hour = datetime.now(timezone('Asia/Tashkent')).strftime("%H")
    now_min = datetime.now(timezone('Asia/Tashkent')).strftime("%M")

    now_time = int(now_hour) * 60 + int(now_min)

    if day != today or now_time - last_time > 30:
        sms = totaldata()
    else:
        out_file = open("Totaldata.txt", "r")
        sms = out_file.read()

    sms = dtime + '\n\n' + sms + '\n\n' + "Manba: worldometers.info"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    total_data = types.KeyboardButton("Umumiy ma'lumot")
    small_data = types.KeyboardButton("Davlatlar bo'yicha ma'lumot")
    help_info = types.KeyboardButton("Yordam\Ko'rsatma")
    markup.add(total_data,small_data)
    markup.add(help_info)
    bot.send_message(message.from_user.id, sms, reply_markup=markup,parse_mode='markdown')
        

@bot.message_handler(content_types=['text'], func = lambda message: message.text == "Davlatlar bo'yicha ma'lumot")

def single(message):
    msg = message.text
    
    msg = bot.send_message(message.from_user.id, "Ma'lumot olmoqchi bo'lgan davlatingiz nomining bosh harfini kiriting")
    bot.register_next_step_handler(msg, harf)
    
 
def harf(message):
    chat_id = message.chat.id
    some = message.text
    letter = some.lower()
    all_letters = "abcdefghijklmnopqrstuvwxyz"

        
    if len(letter) != 1 or not letter.isalpha() or letter not in all_letters:
        msg = bot.reply_to(message, "Kechirasiz, noto'g'ri buyruq kiritildi, faqat bir dona lotin harf kiriting!!!")
        bot.register_next_step_handler(msg, harf)
        return
    
        
    else:
        con = sqlite3.connect('CoronaData.db')

        day = [days for days in con.execute("SELECT Day FROM TIMER")]
        last_time = [times for times in con.execute("SELECT Nowtime FROM TIMER")]

        day = int(day[0][0])
        last_time = int(last_time[0][0])

        today = int(datetime.now(timezone('Asia/Tashkent')).strftime("%d"))
        now_hour = datetime.now(timezone('Asia/Tashkent')).strftime("%H")
        now_min = datetime.now(timezone('Asia/Tashkent')).strftime("%M")

        now_time = int(now_hour) * 60 + int(now_min)

        if day != today or now_time - last_time > 30:
            dat = main_data()
        else:
            dat = [list(row) for row in con.execute("SELECT Country, Virus, New_virus, Dead, New_dead, Recovered, Now_virus, Hard, Checked, Qit FROM CORONA")]
            con.close()

        arr = []
        c = 0
        shower = []

        for item in dat:
            if item[0][0].lower() == letter:
                shower.append(str(str(c) + ' - ' + item[0]))
                arr.append(item)
                c+=1
        countries = '\n'.join(shower)



        bot.send_message(message.from_user.id, countries)
            
        msg = bot.send_message(message.from_user.id, 'Yuqoridagi davlatlar orasidan qidirgan davlatingiz oldidagi raqamlardan birini kiriting')
        bot.register_next_step_handler(msg, son)

        user = User(c, arr)
        user_dict[chat_id] = user
        
            
def son(message):
        
        dtime = datetime.now(timezone('Asia/Tashkent')).strftime("Sana: %d-%m-%Y yil \nSoat: %H:%M dagi holat bo'yicha: ")
                
        numb = message.text

        if len(numb) > 2 or not numb.isdigit():
            msg = bot.reply_to(message, "Kechirasiz, noto'g'ri buyruq kiritildi, faqat yuqoridagi davlatlar oldidagi raqamlardan birini kiriting!!!")
            bot.register_next_step_handler(msg, son)
            return
        else:
            numb = int(numb)
            chat_id = message.chat.id
            user = user_dict[chat_id]
            c = user.qiymat    

            if numb >= c or numb < 0:
                msg = bot.reply_to(message, "Kechirasiz, noto'g'ri buyruq kiritildi, faqat yuqoridagi davlatlar oldidagi raqamlardan birini kiriting")
                bot.register_next_step_handler(msg, son)
                return
            else:
                arr = user.array
                result = []    
                head = ['Davlat ', 'Kasallanganlar ', 'Yangi kasallanganlar ', 'Vafot etganlar ', 'Yangi vafot etganlar ', 'Tuzalganlar ', 'Hozirda kasallar ', "Ahvoli og'irlar ", 'Tekshirilganlar ', "Qit'a "]
    
                for n in range(len(arr)):
                    if n == numb:
                        for i in range(len(head)):
                            arr[n][i] = arr[n][i].replace('+', '')
                            result.append((head[i] + ' : ' + arr[n][i]))
                

                giver = '\n'.join(result)
                giver = dtime + '\n\n' + giver + '\n\n' + "Manba: worldometers.info"

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                total_data = types.KeyboardButton("Umumiy ma'lumot")
                small_data = types.KeyboardButton("Davlatlar bo'yicha ma'lumot")
                help_info = types.KeyboardButton("Yordam\Ko'rsatma")
                markup.add(total_data,small_data)
                markup.add(help_info)
                bot.send_message(message.from_user.id, giver, reply_markup=markup,parse_mode='markdown')
            


@bot.message_handler(content_types=['text'], func = lambda message: message.text == "Yordam\Ko'rsatma")

def helper(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    total_data = types.KeyboardButton("Umumiy ma'lumot")
    small_data = types.KeyboardButton("Davlatlar bo'yicha ma'lumot")
    help_info = types.KeyboardButton("Yordam\Ko'rsatma")
    markup.add(total_data,small_data)
    markup.add(help_info)
    bot.send_message(message.from_user.id, """
Bu bot orqali siz koronavirusdan zararlanganlar soni bo'yicha ma'lumot olishingiz mumkin. Davlatlat boyicha aniq ma'lumot olish uchun istagan davlat nomini bosh harfini kiriting,
shundan so'ng chiqqan ro'yhatdan qidirgan davlatingiz oldidagi raqamni kiriting. Koronavirusga chalinganlar soni ko'paymasligi uchun iltimos \nUYDA QOLING!!!
    """, reply_markup=markup,parse_mode='markdown')

@bot.message_handler(content_types=['text'], func = lambda message: message.text != "Yordam\Ko'rsatma" and message.text != "Umumiy ma'lumot" and message.text != "Davlatlar bo'yicha ma'lumot")
def error(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    total_data = types.KeyboardButton("Umumiy ma'lumot")
    small_data = types.KeyboardButton("Davlatlar bo'yicha ma'lumot")
    help_info = types.KeyboardButton("Yordam\Ko'rsatma")
    markup.add(total_data,small_data)
    markup.add(help_info)
    bot.send_message(message.from_user.id,"""
   Kechirasiz, notog'ri buyruq kiritildi! Iltimos faqat quyidagi tugmalardan birini bosing!
   """,reply_markup=markup,parse_mode='markdown')
    

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
    
