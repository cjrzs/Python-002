"""
coding:utf8
@Time : 2020/8/5 23:13
@Author : cjr
@File : pmap.py
"""
import json
import re
import sys
import subprocess
import telnetlib
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed


# 先获取CPU并发数，如果用户未指定并发数或者超过该并发数则重置最大并发为该数量
# 最大线程数默认为最大进程数 * 5
CPU_COUNT = multiprocessing.cpu_count()


def ping(ip):
    """
    ping一个ip，发送4个包，获取结果
    :param ip:
    :rtype: int
    :return:
    """
    res = {}
    cmd = f'ping -n 4 {ip}'
    try:
        result = subprocess.getoutput(cmd)
    except Exception as e:
        print(f'命令: {cmd} 错误\n{e}')
    if '(0% 丢失)' in result.split('\n')[-3]:
        res[ip] = True
    else:
        res[ip] = False
    return res


def get_ip_status(ip, port):
    """
    获取（IP:port）是否OK
    :param ip:
    :param port:
    :return:
    """
    res = {}
    if not ip:
        ip = '47.105.70.179'
    tel = telnetlib.Telnet()
    try:
        tel.open(ip, port, timeout=2)
        res[f'{ip}:{port}'] = True
    except Exception:
        res[f'{ip}:{port}'] = False
    finally:
        tel.close()
    print(f'ping的结果: {res}')
    return res


def put_queue(q, ips, ports=None, lock=None):
    """
    当使用进程时候，需要用队列通信
    将需要处理的IP，port放入队列
    :param q:
    :param ips:
    :param ports:
    :param lock:
    :return:
    """
    lock.acquire()
    if not ports:
        for ip in ips:
            q.put([ip])
    else:
        for ip in ips:
            for port in ports:
                q.put([ip, port])
    lock.release()


def get_queue(q, func_type=None):
    """
    从队列中取出资源，并交给对应方法处理
    :param q:
    :param func_type:
    :return:
    """
    while True:
        if not q.empty():
            value = q.get(True)
            if func_type == 'ping':
                print(f'是否取到了参数: {value[0]}')
                res = ping(value[0])
                print(f'是否取得了结果: {res}')
            else:
                res = get_ip_status(value[0], value[1])
        else:
            return res


def processing_ip(n, ips):
    """
    多进程处理IP是否可以ping通
    :param n:
    :param ips:
    :return:
    """
    tmp = []
    res = []
    mg = multiprocessing.Manager()
    ip_queue = mg.Queue(len(ips))
    lock = mg.Lock()
    with multiprocessing.Pool(n) as pool:
        pool.apply_async(put_queue, args=(ip_queue, ips, None, lock))
        tmp.append(pool.apply_async(get_queue, args=(ip_queue, 'ping')).get())
        # res.append(result)
    pool.join()
    print(f'tmp: {tmp}')
    for i in tmp:
        res.append(i)
    return res


def processing_port(n, ips, ports):
    """
    多进程处理IP和端口是否OK
    :param n:
    :param ips:
    :param ports:
    :return:
    """
    res = []
    mg = multiprocessing.Manager()
    ip_queue = mg.Queue(len(ips) * len(ports))
    lock = mg.Lock()
    with multiprocessing.Pool(n) as pool:
        pool.apply_async(put_queue, args=(ip_queue, ips, ports, lock))
        result = pool.apply_async(get_queue, args=(ip_queue,))
        res.append(result.get())
    pool.join()
    return res


def thread_port(n, ips, port_list):
    """
    多线程处理IP和端口是否OK
    :param n:
    :param ips:
    :param port_list:
    :return:
    """
    result = []
    with ThreadPoolExecutor(n) as executor:
        for ip in ips:
            for port in port_list:
                all_task = executor.submit(get_ip_status, ip, port)
    for future in as_completed(all_task):
        result.append(future.result())
    return result


def thread_ip(n, ips):
    """
    多线程处理IP
    :param n:
    :param ips:
    :return:
    """
    result = []
    with ThreadPoolExecutor(n) as executor:
        obj_list = []
        for ip in ips:
            task = executor.submit(ping, ip)
            obj_list.append(task)
    for future in as_completed(obj_list):
        result.append(future.result())
    return result


def write_file(file_name, content):
    """
    将结果写入文件
    :param file_name:
    :param content:
    :return:
    """
    with open(file_name, '+w') as f:
        f.writelines(json.dumps(content))
    return '写入文件完成'


class PortScan:
    def __init__(self, params):
        for i in zip(params[1::2], params[2::2]):
            print(i[0], i[1])
            if '-n' in params and i[0] == '-n' and int(i[1]) < CPU_COUNT:
                self.concurrency = i[1]
            else:
                self.concurrency = CPU_COUNT
            if '-f' in params and i[0] == '-f':
                self.func_type = i[1]
            if '-ip' in params and i[0] == '-ip':
                self.ips = self.get_user_output_ip(i[1])
            if '-w' in params and i[0] == '-w':
                self.save_file = i[1]
            else:
                self.save_file = None
            if '-m' in params and i[0] == '-m':
                self.module = i[1]
            else:
                self.module = 'thread'

    @staticmethod
    def get_user_output_ip(output_ips):
        if '-' in output_ips:
            # 先根据"-"分出起始IP和末尾IP
            # 然后根据"."分割取最后一个元素用做range()的边界
            # 最后和前面的IP段拼起来，组合成最终的IP列表
            tmp_ip_list = re.split('-', output_ips)
            start_ip = tmp_ip_list[0].split('.')[-1]
            end_ip = tmp_ip_list[1].split('.')[-1]
            ip_before_three = tmp_ip_list[0].split('.')[:-1]
            result = [f'{".".join(ip_before_three)}.{i}' for i in range(int(start_ip), int(end_ip) + 1)]
        else:
            result = [output_ips]
        return result

    def my_run(self):
        ports = [port for port in range(1, 1025)]
        if not self.ips:
            return '请使用-ip指定IP范围'
        if not self.func_type:
            return '请使用-f指定测试类型'
        if self.func_type == 'ping' and self.module == 'thread':
            result = thread_ip(self.concurrency, self.ips)
        elif self.func_type == 'tcp' and self.module == 'thread':
            result = thread_port(self.concurrency, self.ips, ports)
        elif self.func_type == 'ping' and self.module == 'proc':
            result = processing_ip(self.concurrency, self.ips)
            print('执行的是这个么')
        elif self.func_type == 'tcp' and self.module == 'proc':
            result = processing_port(self.concurrency, self.ips, ports)
        else:
            result = None
        return result


if __name__ == '__main__':
    print(processing_ip(4, ['47.105.70.179']))
    # start_time = time.time()
    # params = sys.argv
    # print(params)
    # x = PortScan(params)
    # result1 = x.my_run()
    # print(f'最终输出结果: {result1}')
    # end_time = time.time()
    # if '-v' in params:
    #     print(end_time - start_time)
    # elif '-w' in params:
    #     file_index = params.index('-w') + 1
    #     file_name = params[file_index]
    #     if result1:
    #         write_file(file_name, result1)


    # print(params)
    # for i in zip(params[1::2], params[2::2]):
    #     print(i)
    #

    # output_ips = [f'47.105.70.{i}' for i in range(150, 180)]
    # output_port_list = [port for port in range(10, 23)]
    # thread_port(4, ips=output_ips, port_list=output_port_list)
    # thread_ip(1, ips=output_ips)
    # thread_ip(2, output_ips)
    # processing_ip(6, output_ips)


