from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

alphabet = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm',
            13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y', 25: 'z'}

specChar = {0: "~", 1: ".", 2: "?", 3: ";", 4: ":", 5: "!", 6: "@", 7: "$", 8: "%", 9: "^", 10: "&", 11: "(",
            12: ")", 13: "+", 14: "-", 15: "*", 16: "/", 17: "<", 18: ">", 19: "`", 20: "#", 21: "\"", 22: "'", 23: ","}


def isSpecialChar(element):
    return element in specChar.values()


def isCharacter(element):
    return element.lower() in alphabet.values()


def isNumber(element):
    return element.isdigit()


def encrypt(message, encryptNum):
    encryptedMessage = ""

    for mElement in message:
        if mElement == " ":
            encryptedMessage = encryptedMessage + " "
        elif mElement == ".":
            encryptedMessage = encryptedMessage + "."
        elif isSpecialChar(mElement):
            for aCharacter in specChar:
                if mElement == specChar[aCharacter]:
                    eChar = (aCharacter + encryptNum) % 24
                    encryptedMessage = encryptedMessage + specChar[eChar]
        elif isCharacter(mElement):
            for aLetter in alphabet:
                if mElement.lower() == alphabet[aLetter]:
                    eLetter = (aLetter + encryptNum) % 26
                    encryptedMessage = encryptedMessage + alphabet[eLetter]
        elif isNumber(mElement):
            eNumber = (int(mElement) + encryptNum) % 10
            encryptedMessage = encryptedMessage + str(eNumber)
        else:
            encryptedMessage = encryptedMessage + mElement

    return encryptedMessage


def decrypt(message, decryptNum):
    decryptedMessage = ""

    for mElement in message:
        if mElement == " ":
            decryptedMessage = decryptedMessage + " "
        elif mElement == ".":
            decryptedMessage = decryptedMessage + "."
        elif isSpecialChar(mElement):
            for aCharacter in specChar:
                if mElement == specChar[aCharacter]:
                    deChar = (aCharacter - decryptNum) % 24
                    decryptedMessage = decryptedMessage + specChar[deChar]
        elif isCharacter(mElement):
            for aLetter in alphabet:
                if mElement.lower() == alphabet[aLetter]:
                    deLetter = ((aLetter - decryptNum) % 26)
                    decryptedMessage = decryptedMessage + alphabet[deLetter]
        elif isNumber(mElement):
            deNumber = (int(mElement) - decryptNum) % 10
            decryptedMessage = decryptedMessage + str(deNumber)
        else:
            decryptedMessage = decryptedMessage + mElement

    return decryptedMessage


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    message = request.form['message']
    encrypt_num = int(request.form['encrypt_num'])

    # Restricting the encryption number to the range 1 to 25
    encrypt_num = max(1, min(encrypt_num, 25))

    encrypted_message = encrypt(message, encrypt_num)
    return render_template('result.html', result=encrypted_message)


@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    message = request.form['message']
    decrypt_num = int(request.form['decrypt_num'])

    # Restricting the decryption number to the range 1 to 25
    decrypt_num = max(1, min(decrypt_num, 25))

    decrypted_message = decrypt(message, decrypt_num)
    return render_template('result.html', result=decrypted_message)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
