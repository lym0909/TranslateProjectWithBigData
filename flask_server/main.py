# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from flask import Flask
from flask import render_template
from werkzeug.datastructures import ImmutableMultiDict
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from translate import translate_ms
from translate import getDB
from translate import getStatisticData
import json

app = Flask(__name__)

@app.route('/history')
def returnHistoryTemplate():
	data = getDB()
	return render_template('history.html', data=data)
	
@app.route('/statistics')
def returnStatisticsTemplate():
	info = getStatisticData()
	
	return render_template('statistics.html', enToko=info[0], koToja=info[1], koToca=info[2], enToja=info[3], enToca=info[4], koTofr=info[5], koToda=info[6], koToen=info[7])
	
@app.route('/infomation')
def returnInfoTemplate():
	return render_template('infomation.html')
    
@app.route('/translate')
def returnMainTemplate():
	return render_template('translate.html')

@app.route('/translate/<langFrom>/<langTo>/<senten>', methods=['GET'])
def returnTransFromFullURL(langFrom, langTo, senten):
    return translate_ms(senten, langFrom, langTo) #return json
    
@app.route('/test', methods=['POST'])
def test():
	data = getDB()
	
	for a in data:
		print a['original'], a['result'], a['from_lang'], a['to_lang']

@app.route('/translate', methods=['POST'])
def returnTransFromPOST():
    if request.method == 'POST':
    	data = request.form
        #from_lang = request.form['from']
        #to_lang = request.form['to']
        #string = request.form['original']
        
    _data = dict(data)
    
    if _data['from'][0] == u'--------선택하세요--------':
    	return render_template('translate.html')
    elif _data['to'][0] == u'--------선택하세요--------':
    	return render_template('translate.html')
    
    return render_template('translate.html', result=returnTransResult(_data['original'][0], _data['from'][0], _data['to'][0]), original=_data['original'][0])
    
def returnTransResult(string, lang_from, lang_to):
	return (json.loads(translate_ms(string, lang_from, lang_to))['result'])

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
