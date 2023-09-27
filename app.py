from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def normalize_phone_number(phone_number):
    phone_number = ''.join(filter(lambda char: char.isdigit() or char in '/-', phone_number))

    if phone_number.startswith("01"):
        phone_number = "+431" + phone_number[2:]

    phone_number = phone_number.lstrip('0').replace('00', '+')

    if phone_number.startswith('(0043)(0)'):
        phone_number = '+43' + phone_number[9:]

    if phone_number.startswith('+43(0)'):
        phone_number = '+43' + phone_number[5:]

    if not phone_number.startswith('+43') and '43' in phone_number:
        phone_number = '+43' + phone_number.replace('43', '', 1)

    if phone_number.startswith('+43'):
        phone_number = '+43' + phone_number[3:].lstrip('0')


    if not phone_number.startswith('+43'):
        phone_number = '+43' + phone_number


    phone_number = phone_number.replace('/', '').replace('-', '')
    # if len(phone_number) > 10:
    #     phone_number = phone_number[:-7] + ' ' + phone_number[-7:-5] + ' ' + phone_number[-5:]
    return phone_number
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/normalize-phone', methods=['POST'])
def normalize_phone():
    try:
        data = request.get_json()
        if 'phone_number' in data:
            phone_number = data['phone_number']
            normalized_number = normalize_phone_number(phone_number)
            return jsonify({'normalized_phone_number': normalized_number})
        else:
            return jsonify({'error': 'Phone number missing in the request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)







