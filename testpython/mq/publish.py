# -*- coding:utf-8 -*-
# @author wuhao
# @date 2022/2/24
import sys

import pika

rabbit_user = "guest"
rabbit_password = "guest"
rabbit_address = "10.2.11.234"
rabbit_port = 5672
exchange_name = 'logs'
receive_order_queue = "tests"

# 创建凭证，使用rabbitmq用户密码登录 # 去邮局取邮件，必须得验证身份
credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
# 新建连接，这里localhost可以更换为服务器ip # 找到这个邮局，等于连接上服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_address, rabbit_port, '/', credentials))
# 创建频道 # 建造一个大邮箱，隶属于这家邮局的邮箱，就是个连接
channel = connection.channel()


def base_publish():
    # 声明一个队列，用于接收消息，队列名字叫“水许传”
    channel.queue_declare(queue='SH4', durable=True)
    # 注意在rabbitmq中，消息想要发送给队列，必须经过交换(exchange)，初学可以使用空字符串交换(exchange=‘‘)，
    # 它允许我们精确的指定发送给哪个队列(routing_key=‘‘),参数body值发送的数据
    # delivery_mode=2代表消息持久化
    channel.basic_publish(exchange="",
                          routing_key="SH4",
                          body="SH4 持久化 来啦来啦！",
                          # 数据持久化
                          properties=pika.BasicProperties(delivery_mode=2))
    print("已经发送了消息")
    # 程序退出前，确保刷新网络缓冲以及消息发送给rabbitmq，需要关闭本次连接
    connection.close()


# fanout纯广播/all
# 需要queue和exchange绑定，因为消费者不是和exchange直连的，消费者连接在queue上，queue绑定在exchange上，消费者只会在queue里读取消息。
def publish1():
    # 这里是广播，不需要声明queue
    channel.exchange_declare(exchange="log",  # 声明广播管道
                             exchange_type="fanout")
    # delivery_mode=2代表消息持久化
    channel.basic_publish(exchange="log",
                          routing_key="",  # 此处为空，必须有
                          body="fanout 持久化 来啦来啦！")
    print("消息发送完成")
    connection.close()


# direct 路由模式，通过routing_key将消息发送给对应的queue
def publish2():
    # 这里是广播，不需要声明queue
    channel.exchange_declare(exchange="direct_logs",  # 声明广播管道
                             exchange_type="direct")
    # 重要程度级别，这里默认定义为 info
    severity = sys.argv[1] if len(sys.argv) & 1 else 'info'
    message = ''.join(sys.argv[2:]) or 'Hello World!'

    channel.basic_publish(exchange="direct_logs",
                          routing_key=severity,
                          body=message)
    print(" [x] Sent %r:%r" % (severity, message))
    connection.close()


# topic模式类似于direct模式，只是其中的routing_key变成了一个有“.”分隔的字符串，“.”将字符串分割成几个单词  # 每个单词代表一个条件
def publish3():
    pass


# 关键字发布 即：队列绑定关键字，发送者将数据根据关键字发送到消息exchange，exchange根据关键字判定应该将数据发送至指定队列
def publish4():
    # 这里是广播，不需要声明queue
    channel.exchange_declare(exchange='m2', exchange_type='direct')
    channel.basic_publish(exchange="m2",
                          routing_key="vita",
                          body="vita send message")
    print("消息发送完成")
    connection.close()


if __name__ == "__main__":
    publish1()
