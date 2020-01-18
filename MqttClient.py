#!/usr/bin/env python3
# encoding:utf-8

# 需要安装mqtt
# pip install paho-mqtt
import paho.mqtt.client as mqtt
import socket
import json
import logging
import threading

# 设置日志文件和日志级别
logging.basicConfig(filename='mqttClientPython3.log', level=logging.DEBUG)

# 服务器IP
SERVER_HOST = '183.230.40.39'
# 服务器端口
SERVER_PORT = 6002
# 设备id
CLIENT_ID = ''
# 产品id
PRODUCT_ID = ''
# 鉴权key
API_KEY = ''

DEVICE_ID = CLIENT_ID
USERNAME = PRODUCT_ID
PASSWORD = API_KEY

# mqttClient 全局对象
client = None

# first
FIRST = 5
# loop
LOOP = 30


# 客户端从服务器收到CONNACK响应时的回调。
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$dp")


# 从服务器收到发布消息时的回调
def on_message(client, userdata, msg):
    logging.debug('TOPIC:[%s] PAYLOAD:[%s]', msg.topic, str(msg.payload))


# onenet 类型3
def one_net_payload_type3(msg_obj):
    logging.debug('msg_obj:[%s]', msg_obj)
    # 转成json字符串
    msg_str = json.dumps(msg_obj)
    # 获取字符串长度
    msg_len = msg_str.__len__()

    logging.debug('msg_len:[%s]', msg_len)

    # 构建payload
    payload_bytes = bytearray(msg_str.encode(encoding='UTF-8'))
    payload_bytes.insert(0, 3)
    payload_bytes.insert(1, msg_len >> 8)
    payload_bytes.insert(2, msg_len & 0x00FF)

    logging.debug('payload_bytes:[%s]', payload_bytes)
    return payload_bytes


# 获取自身的IP地址
def get_host_ip():
    logging.debug('Get ip')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        logging.debug('ip:[%s]', ip)
    finally:
        s.close()
    return ip


# 初始化mqtt
def mqtt_init():
    logging.debug('mqtt_init start')
    global client
    #  创建一个MQTT客户端对象
    client = mqtt.Client(client_id=CLIENT_ID)
    # 设置连接回调
    client.on_connect = on_connect
    # 设置收到消息回调
    client.on_message = on_message

    # 设置连接
    client.connect(SERVER_HOST, SERVER_PORT, 60)
    # 设置认证
    client.username_pw_set(USERNAME, PASSWORD)
    # 订阅
    client.publish(topic='$dp')
    logging.debug('mqtt_init end')


def do_something():
    global client
    logging.debug('do_something start')
    data = {
        'ip': get_host_ip()
    }
    payload = one_net_payload_type3(data)

    client.publish(topic='$dp', payload=payload)

    timer = threading.Timer(LOOP, do_something)
    timer.start()
    logging.debug('do_something end')


if __name__ == '__main__':
    logging.debug('system start')
    mqtt_init()
    logging.debug('schedule')

    timer = threading.Timer(FIRST, do_something)
    timer.start()

    logging.debug('mqtt_loop_forever')
    # 阻止处理网络流量，调度回调和
    # 处理重新连接。
    # 其他loop *（）函数可用，这些函数提供了线程接口和
    # 手动界面。
    client.loop_forever()

    logging.debug('end')
