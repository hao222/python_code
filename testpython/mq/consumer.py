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

# 建立与rabbitmq的连接
credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
# 新建连接，这里localhost可以更换为服务器ip # 找到这个邮局，等于连接上服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_address, rabbit_port, '/', credentials))
# 创建频道 # 建造一个大邮箱，隶属于这家邮局的邮箱，就是个连接
channel = connection.channel()


def base_consumer():
    channel.queue_declare(queue="SH4", durable=True)

    def callback(ch, method, properties, body):
        print("消费者接收到了任务：%r" % body.decode("utf8"))
        ch.basic_ack(delivery_tag=method.delivery_tag)

        # 有消息来临，立即执行callback，没有消息则夯住，等待消息
        # 老百姓开始去邮箱取邮件啦，队列名字是水许传

    # def basic_consume(self,
    #                       queue,
    #                       on_message_callback,
    #                       auto_ack=False,
    #                       exclusive=False,
    #                       consumer_tag=None,
    #                       arguments=None):
    # 这个参数的调用有所改动
    # 第一个参数是队列
    # 第二个是回调函数
    # 第三个这是auto_ack=True
    channel.basic_consume("SH4", callback, False)
    # 开始消费，接收消息
    channel.start_consuming()


# fanout纯广播模式/all
def consumer1():
    channel.exchange_declare(exchange="log", exchange_type="fanout")
    # exclusive=True会在使用此queue的消费者断开后，自动将queue删除
    result = channel.queue_declare(queue="", exclusive=True)
    # 获取随机的queue名字
    queue_name = result.method.queue
    print("random queuename", queue_name)
    channel.queue_bind(exchange="log",  # queue绑定到转发器上
                       queue=queue_name)

    def callback(ch, method, properties, body):
        print("消费者接收到了任务：%r" % body.decode("utf8"))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # auto_ack设置为False
    channel.basic_consume(queue_name, callback, False)
    # 开始消费，接收消息
    channel.start_consuming()


def consumer2():
    # 生产者和消费者端都要声明队列，以排除生成者未启动，消费者获取报错的问题
    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")
    # 不指定queue名字，rabbit会随机分配一个名字
    # exclusive=True会在使用此queue的消费者断开后，自动将queue删除
    result = channel.queue_declare(queue="", exclusive=True)
    # 获取随机的queue名字
    queue_name = result.method.queue
    print("random queuename", queue_name)
    severities = sys.argv[1:]
    # if not severities:
    #     sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    #     sys.exit(1)
    if not severities:
        severities = ['info', ]
    # 循环列表去绑定
    for severity in severities:
        print(severity)
        channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)
        print("Waiting for log!")

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    # auto_ack设置为False
    channel.basic_consume(queue_name, callback, True)
    # 开始消费，接收消息
    channel.start_consuming()


# topic 正则匹配
def consumer3():
    pass


# 关键字发布
def consumer4():
    channel.exchange_declare(exchange="m2", exchange_type="direct")
    # 不指定queue名字，rabbit会随机分配一个名字
    # exclusive=True会在使用此queue的消费者断开后，自动将queue删除
    result = channel.queue_declare(queue="", exclusive=True)
    # 获取随机的queue名字
    queue_name = result.method.queue
    print("random queuename", queue_name)
    # 让exchange和queque进行绑定.
    channel.queue_bind(exchange='m2', queue=queue_name, routing_key='lili')
    channel.queue_bind(exchange='m2', queue=queue_name, routing_key='vita')

    def callback(ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    # auto_ack设置为False
    channel.basic_consume(queue_name, callback, True)
    # 开始消费，接收消息
    channel.start_consuming()


if __name__ == "__main__":
    # 只有绑定 和publish 一样的路由才能获取到数据 routing_key 一致
    consumer1()
