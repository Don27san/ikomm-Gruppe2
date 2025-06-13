# This script shows the basic functionality of data encoding

def ascii_introduction():
    text = "Lehrstuhl für Kommunikationsnetze"
    print("------------------------ Data ------------------------")
    print("Data:", text)
    print("Type of data:", type(text))

    # Encoding to ASCII
    print("-------------------- ASCII encoded --------------------")
    try:
        data = text.encode('ASCII')  # This will raise an exception
    except Exception as e:
        print("ASCII encoding error:", e)
        print("ASCII only allows certain letters to be encoded according to the ASCII alphabet. For example Ä, Ö and Ü "
              "are not part of this alphabet.")

    # Using UTF-8 as fallback
    print("-------------------- UTF-8 encoded --------------------")
    data = text.encode('UTF-8')
    try:
        print(data.decode('ASCII'))  # This will also raise an exception
    except Exception as e:
        print("ASCII decoding error:", e)
    
    print("Decoded from UTF-8:", data.decode('UTF-8'))


if __name__ == '__main__':
    ascii_introduction()
