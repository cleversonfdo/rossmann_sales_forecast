import os
import requests
import json
import pandas as pd

from flask import Flask, request, Response

# constants
TOKEN = '5123518599:AAEnQzt3i35c5lUhtQPc_-2tjD3di541uoI'

# Info about bot
#https://api.telegram.org/bot5123518599:AAEnQzt3i35c5lUhtQPc_-2tjD3di541uoI/getMe

# Get updates
#https://api.telegram.org/bot5123518599:AAEnQzt3i35c5lUhtQPc_-2tjD3di541uoI/getUpdates

# Set Webhook
#https://api.telegram.org/bot5123518599:AAEnQzt3i35c5lUhtQPc_-2tjD3di541uoI/setWebhook?url=https://rossmann-bot-cleversonfdo.herokuapp.com

# send message
#https://api.telegram.org/bot5123518599:AAEnQzt3i35c5lUhtQPc_-2tjD3di541uoI/sendMessage?chat_id=1051749277&text=Hi Work

def send_message(chat_id, text):
	url = 'https://api.telegram.org/bot{}/'.format(TOKEN)
	url = url + 'sendMessage?chat_id={}'.format(chat_id)

	r = requests.post(url, json = {'text':text})
	print('Status Code {}'.format(r.status_code))
 	
	return None	


def load_dataset(store_id):

	# loading test dataset
	#df10 = pd.read_csv('/home/work/Documents/repos/curso_data_science_em_producao/data/test.csv')
	df10 = pd.read_csv('test.csv')
	#df_store_raw = pd.read_csv('/home/work/Documents/repos/curso_data_science_em_producao/data/store.csv')
	df_store_raw = pd.read_csv('store.csv')

	# merge test dataset + store
	df_test = pd.merge(df10, df_store_raw, how = 'left', on = 'Store')

	# choose store for prediction
	#df_test = df_test[df_test['Store'].isin([4, 23, 25 ])]
	df_test = df_test[df_test['Store'] == store_id]

	if not df_test.empty:
	
		# remove closed days
		df_test = df_test[df_test['Open'] != 0]
		df_test = df_test[~df_test['Open'].isnull()]
		df_test = df_test.drop('Id', axis = 1)

		# converting dataframe to jason, for transmiting the archive between instances
		data = json.dumps(df_test.to_dict(orient = 'records'))
	else:
		data = 'error'
		
	return data
	
def predict(data):

	# API call
	#url = 'http://0.0.0.0:5000/rossmann/predict'
	url = 'https://rossmann-model-cleversonfdo.herokuapp.com/rossmann/predict'
	header = {'Content-type' : 'application/json'}
	data = data

	r = requests.post(url, data, headers = header)
	print('Status Code {}'.format(r.status_code))

	d1 = pd.DataFrame(r.json(), columns = r.json()[0].keys())
	
	return d1

def parse_message(message):
	chat_id = message['message']['chat']['id']
	store_id = message['message']['text']
	
	store_id = store_id.replace('/', '')
       
	try: # checando se o valor enviado é um numero de loja
		store_id = int(store_id)
       	
	except ValueError:
       	
		store_id = 'error'

	return chat_id, store_id


# API initialize
app = Flask(__name__)

# endpoint
@app.route('/', methods = ['GET', 'POST'])
def index(): # irá rodar toda vez que o endpoint rodar
	if request.method == 'POST':
		message = request.get_json()
		
		chat_id, store_id = parse_message(message)
		
		if store_id != 'error':
			# loading data
			data = load_dataset(store_id)
			
			if data != 'error':
			
				# prediction
				d1 = predict(data)
			
				# calculation
				d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()

				# send message
				msg = 'Store Number {} will sell R${:,.2f} in the next 6 weeks'.format(d2['store'].values[0], d2['prediction'].values[0])
    					
				send_message(chat_id, msg)
    				
				return Response('Ok', status = 200)
				
				
			else:
				send_message(chat_id, 'Store Not Available')
				return Response('Ok', status = 200)
		else:
			send_message(chat_id, 'Store ID is Wrong')
			return Response('Ok', status = 200) # o status informa para a api que finalizou
		
	else:
		return '<h1> Rossmann Telegram BOT </h1>'
		
		

if __name__ == '__main__':
	port = os.environ.get('PORT', 5000) # o heroku não sabe que porta é a 5000, precisa-se passar
	app.run(host = '0.0.0.0', port = port) # to run the api
