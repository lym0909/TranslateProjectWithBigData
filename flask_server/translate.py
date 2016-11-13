#-*- coding: utf-8 -*-

from mstranslator import Translator
from dateTime import getCurrentDate
from dateTime import getCurrentTime

import sys
import goslate
import json
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')

CLIENT_ID = "translatelate"
CLIENT_SECRET = "GK7MyfCoz1NUrNuehRZBlLWLNpHMgDaAZoT8MkQOMlI="
translator_ms = Translator(CLIENT_ID, CLIENT_SECRET)

languages = ["af", "sq", "ar","be", "bg", "ca", "zh-CN", "zh-TW", "hr",
             "cs", "da", "nl", "en", "et", "tl", "fi", "fr", "gl", "de",
             "el", "iw", "hi", "hu", "is", "id", "ga", "it", "ja", "ko",
             "lv", "lt", "mk", "ms", "mt", "no", "fa", "pl", "pt", "ro",
             "ru", "sr", "sk", "sl", "es", "sw", "sv", "th", "tr", "uk",
             "vi", "cy", "yi"]

def validateLanguage(lang):
    if lang in languages:
        return True
    return False

def saveData(host, user, passwd, db, result, original, from_lang, to_lang, tableName):
    dBase = MySQLdb.connect(host, user, passwd, db, charset='utf8', use_unicode=True)
    cursor = dBase.cursor()

    string_1 = 'insert into %s(result, original, date, time, from_lang, to_lang) ' % (tableName)
    string_2 = 'values("%s", "%s", "%s", "%s", "%s", "%s")' % (result, original, getCurrentDate(), getCurrentTime(), from_lang, to_lang)

    cursor.execute("use " + db)
    cursor.execute(string_1 + string_2)
    dBase.commit()

    cursor.close()
    dBase.close()

def translate_ms(mstr, lang_from, lang_to):
    result = translator_ms.translate(mstr, lang_from, lang_to)
    result_str = str(result)
    forReturn = {"result":result_str,
                 "original":mstr}

    saveData('localhost', 'root', '0000', 'python_test', result_str, mstr, lang_from, lang_to, 'test')
    
    return json.dumps(forReturn, ensure_ascii=False)

        
def getDB():
	dBase = MySQLdb.connect('localhost', 'root', '0000', 'python_test', charset='utf8', use_unicode=True)
	cursor = dBase.cursor(MySQLdb.cursors.DictCursor)
	
	cursor.execute("use " + "python_test")
	cursor.execute("select * from " + "test")
	
	dbData = cursor.fetchall()
	
	dBase.commit()
	
	cursor.close()
	dBase.close()
	
	return dbData	
	
def getStatisticData():
	
	enToko = 0
	
	koToja = 0
	koToca = 0
	
	enToja = 0
	enToca = 0
	
	koTofr = 0
	koToda = 0
	
	koToen = 0
	
	data = getDB()
	
	for a in data:
		if a['from_lang'] == 'en' and a['to_lang'] == 'ko':
			enToko+=1
		if a['from_lang'] == 'ko' and a['to_lang'] == 'ja':
			koToja+=1
		if a['from_lang'] == 'ko' and a['to_lang'] == 'ca':
			koToca+=1
		if a['from_lang'] == 'en' and a['to_lang'] == 'ja':
			enToja+=1
		if a['from_lang'] == 'en' and a['to_lang'] == 'ca':
			enToca+=1
		if a['from_lang'] == 'ko' and a['to_lang'] == 'fr':
			koTofr+=1
		if a['from_lang'] == 'ko' and a['to_lang'] == 'da':
			koToda+=1
		if a['from_lang'] == 'ko' and a['to_lang'] == 'en':
			koToen+=1
			
	info = [enToko, koToja, koToca, enToja, enToca, koTofr, koToda, koToen]
	return info

		
		