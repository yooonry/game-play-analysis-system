from urllib import parse
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

RIOT_API_KEY = os.getenv('RIOT_API_KEY')

@app.route('/')
def index():
    print(f"API KEY = {RIOT_API_KEY}")
    return render_template('search.html')
    return 'Riot Games API Example'

@app.route('/summoner', methods=['GET'])
def get_summoner_info():
    summoner_name = request.args.get('summoner_name')
    if not summoner_name:
        return jsonify({'error': 'Summoner name is required'}), 400
    print(summoner_name)
    id = parse.quote(summoner_name)
    url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{id}?api_key={RIOT_API_KEY}'

    response = requests.get(url)
    
    if response.status_code == 200:
        summoner_data = response.json()
        profile = summoner_data['profileIconId']
        profile_url = f'https://ddragon.leagueoflegends.com/cdn/13.16.1/img/profileicon/{profile}.png'
        return render_template('index.html', profile_url=profile_url, summoner_data=summoner_data)
    elif response.status_code == 404:
        return jsonify({'error': 'Summoner not found'}), 404
    else:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)