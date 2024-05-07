import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# structure of weather json
weather_data = {
    'temperature': '50 F',
    'humidity': '60%', 
    'wind_speed': '10km/h',
    'description': 'Sunny'
}

temp = "50"

@app.route('/weather', methods=['POST'])
def get_weather():
    if request.is_json:
        req_data = request.json
        if 'city' in req_data and 'date' in req_data:
            city = req_data['city']
            date = req_data['date']
            
            # set the temperature to value from input
            weather_data['temperature'] = f'{temp} F'
                        
            return jsonify({'city': city, 'date': date, 'weather': weather_data})

        return jsonify({'error': 'Invalid request format or missing params'}), 400

if __name__ == '__main__':
    # start server in a thread so it can run while requesting user input
    server_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5001))
    server_thread.start()

    while True:
        # request user input
        temp = input()

        if temp == "exit":
            break

    server_thread.join()
