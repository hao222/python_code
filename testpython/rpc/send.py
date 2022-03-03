# -*- coding:utf-8 -*-
# @author wuhao
# @date 2022/2/25

import queue
import pika
import uuid
import time


class FibRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        # 1.创建连接
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
        self.channel = self.connection.channel()
        # 2.生成随机queue
        # exclusive = True,消费者端断开连接，队列删除
        result = self.channel.queue_declare(queue="", exclusive=True)
        # 随机获取queue名字，发送数据给消费端
        self.callback_queue = result.method.queue
        # self.on_response回调函数:只要收到消息就调用这个函数
        # 声明收到消息后，收queue=self.callback_queue内的消息
        self.channel.basic_consume(self.callback_queue, self.on_response, True)

    def on_response(self, ch, method, props, body):
        """
        收到消息就调用该函数
        :param ch: 管道内存对象
        :param method: 消息发送给哪个queue
        :param props:
        :param body: 数据对象
        :return:
        """
        # 判断随机生成的ID与消费者端发过来的ID是否相同，
        if self.corr_id == props.correlation_id:
            # 将body值给self.response
            print("接收到客户端发送的信息：", body)
            self.response = body

    def call(self, n):
        # 赋值变量，一个循环值
        self.response = None
        # 随机生成唯一的字符串
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange="",
                                   routing_key="rpc_queue",
                                   properties=pika.BasicProperties(
                                       # 告诉消费端，执行命令成功后把结果返回给该队列
                                       reply_to=self.callback_queue,
                                       # 生成UUID，发送给消费端
                                       correlation_id=self.corr_id,
                                   ),
                                   # 发的消息，必须传入字符串，不能传数字
                                   body=str(n))
        # 没有数据就循环接收数据
        while self.response is None:
            # 非阻塞版的start_consuming()
            # 没有消息不会阻塞
            self.connection.process_data_events()
            print("client does not send data")
            time.sleep(1)
        # 接收到了消费端的结果，返回
        return int(self.response)


fib_rpc = FibRpcClient()
print("[x] Requesting fib(6)")
response = fib_rpc.call(6)
print(" [.] Got %r" % response)
