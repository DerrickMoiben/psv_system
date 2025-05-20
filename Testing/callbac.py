from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mpesa/callback', methods=['POST'])
def handle_callback():
    callback_data = request.json

    # Print the callback data to the terminal
    print(callback_data)

    # Return a response to the M-Pesa server
    response_data = {'status': 'success'}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)