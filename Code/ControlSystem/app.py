from flask import Flask, request, jsonify
from flask_cors import CORS
import serial
import serial.tools.list_ports
import time

app = Flask(__name__)
CORS(app) 

serialData = ''
ser = None

@app.route('/', methods=['GET'])
def test():
    return jsonify({'msg': 'Test Good'}), 200

@app.route('/get_ports', methods=['GET'])
def get_ports():
    avaiPorts = []
    for port in serial.tools.list_ports.comports():
        avaiPorts.append(port.name)
    return jsonify({'ports': avaiPorts}), 200

@app.route('/connect_port', methods=['POST'])
def connect():
    data = request.get_json()
    com = data['com']
    bandrate = data['bandrate']
    global ser
    ser = serial.Serial(com, int(bandrate), timeout=0.2)
    if ser.isOpen():
        return jsonify({'msg': '成功连接'}), 200
    else:
        return jsonify({'msg': '连接串口失败'}), 401
    
@app.route('/disconnect_port', methods=['GET'])
def disconnect():
    global ser
    if ser and ser.isOpen():
        ser.close()
        return jsonify({'msg': '成功断开连接'}), 200
    else:
        return jsonify({'msg': '断开连接失败，没有连接'}), 401
    
@app.route('/write', methods=['POST'])
def port_write():
    global ser
    data = request.get_json()
    message = data['message']
    if ser and ser.isOpen():
        ser.write(message.encode('utf-8'))
        return jsonify({'msg': '成功断开连接'}), 200
    else:
        return jsonify({'msg': '发送失败，没有连接'}), 401
    
@app.route('/read', methods=['GET'])
def port_read():
    global ser
    if ser and ser.isOpen():
        while True:
            com_input = ser.readline()
            if (com_input):
                return jsonify({'msg': time.strftime('[%H:%M:%S] ', time.localtime()) + com_input.decode('utf-8')}), 200
            else:
                return jsonify({'msg': ''}), 200
    else:
        return jsonify({'msg': '读取失败，没有连接'}), 401

if __name__ == '__main__':
    app.run(debug=True)