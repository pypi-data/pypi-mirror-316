import pymysql
from pymysql.cursors import DictCursor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
from typing import List, Dict
import json
from dbutils.pooled_db import PooledDB
from concurrent.futures import ThreadPoolExecutor
import queue
from threading import Event

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'encryption_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)

class DataEncryptor:
    def __init__(self, 
                 fields_to_encrypt=None,
                 batch_size=1000,
                 table_name='solid_order_main_wrong',
                 max_workers=4,
                 queue_size=10,
                 checkpoint_file='encryption_checkpoint.json',
                 timeout=30,  # 队列超时时间
                 invalid_dates=None  # 无效日期列表
                 ):
        """
        初始化加密处理器
        
        Args:
            fields_to_encrypt (list): 需要加密的字段列表
            batch_size (int): 每批处理的记录数
            table_name (str): 要处理的表名
            max_workers (int): 工作线程数
            queue_size (int): 队列大小
            checkpoint_file (str): 断点续传文件路径
            timeout (int): 队列等待超时时间(秒)
            invalid_dates (list): 需要处理的无效日期列表
        """
        # 加载环境变量
        load_dotenv()
        
        # 设置加密字段
        self.fields_to_encrypt = fields_to_encrypt or ['dirver_phone', 'trans_number']
        
        # 设置处理参数
        self.batch_size = batch_size
        self.table_name = table_name
        self.max_workers = max_workers
        self.queue_size = queue_size
        self.checkpoint_file = checkpoint_file
        self.timeout = timeout
        
        # 设置无效日期列表
        self.invalid_dates = invalid_dates or [
            '0000-00-00 00:00:00', 
            '0000-00-00', 
            '1000-01-01 00:00:00'
        ]
        
        # 初始化数据库连接和加密
        self.setup_encryption()
        self.setup_database_pools()
        
        # 初始化线程控制
        self.data_queue = queue.Queue(maxsize=self.queue_size)
        self.stop_event = Event()

    def setup_encryption(self):
        """设置确定性加密"""
        # 从环境变量获取密钥
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            # 生成32字节(256位)的密钥
            key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            with open('.env', 'a') as f:
                f.write(f'\nENCRYPTION_KEY={key}\n')
        
        # 确保密钥是32字节
        key_bytes = base64.urlsafe_b64decode(key.encode())
        if len(key_bytes) != 32:
            raise ValueError("密钥必须是32字节(256位)")
            
        # 使用固定的IV以确保加密结果一致
        self.iv = b'\x00' * 16
        self.key = key_bytes
        
    def encrypt_value(self, value: str) -> str:
        """确定性加密单个值"""
        if not value:
            return value
            
        try:
            # 创建加密器
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(self.iv),
                backend=default_backend()
            )
            
            # 填充数据
            padder = padding.PKCS7(128).padder()
            value_bytes = str(value).strip().encode()
            padded_data = padder.update(value_bytes) + padder.finalize()
            
            # 加密
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            
            # 转换为base64字符串
            return base64.urlsafe_b64encode(encrypted_data).decode()
            
        except Exception as e:
            logging.error(f"加密值 {value} 失败: {str(e)}")
            return None

    def setup_database_pools(self):
        """设置数据库连接池"""
        init_command = "SET sql_mode='ALLOW_INVALID_DATES'"
        
        self.local_pool = PooledDB(
            creator=pymysql,
            maxconnections=5,
            host=os.getenv('local_host'),
            user=os.getenv('local_user'),
            password=os.getenv('local_password'),
            database=os.getenv('local_database'),
            cursorclass=DictCursor,
            init_command=init_command  # 添加初始化命令
        )
        
        self.remote_pool = PooledDB(
            creator=pymysql,
            maxconnections=5,
            host=os.getenv('remote_host'),
            user=os.getenv('remote_user'),
            password=os.getenv('remote_password'),
            database=os.getenv('remote_database'),
            cursorclass=DictCursor
        )

    def get_last_processed_id(self) -> int:
        """获取上次处理到的ID"""
        try:
            with open(self.checkpoint_file, 'r') as f:
                checkpoint = json.load(f)
                return checkpoint.get('last_id', 0)
        except FileNotFoundError:
            return 0

    def save_checkpoint(self, last_id: int):
        """保存处理进度"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({'last_id': last_id}, f)

    def encrypt_data(self, data: Dict) -> Dict:
        """加密单条数据"""
        encrypted_data = data.copy()
        for field in self.fields_to_encrypt:
            if field in encrypted_data and encrypted_data[field]:
                encrypted_data[field] = self.encrypt_value(encrypted_data[field])
        return encrypted_data

    def producer(self, remote_conn):
        """生产者：从远程数据库读取数据"""
        try:
            with remote_conn.cursor() as cursor:
                last_id = self.get_last_processed_id()
                
                while not self.stop_event.is_set():
                    cursor.execute(
                        f"SELECT COUNT(*) as count FROM {self.table_name} WHERE id > %s",
                        (last_id,)
                    )
                    remaining_count = cursor.fetchone()['count']
                    
                    if remaining_count == 0:
                        logging.info("没有更多数据需要处理")
                        break

                    cursor.execute(
                        f"SELECT * FROM {self.table_name} WHERE id > %s ORDER BY id LIMIT %s",
                        (last_id, self.batch_size)
                    )
                    batch = cursor.fetchall()
                    
                    if not batch:
                        break

                    self.data_queue.put((batch, last_id))
                    last_id = batch[-1]['id']
                    logging.info(f"已读取数据至ID: {last_id}, 剩余记录数: {remaining_count}")
                    
        except Exception as e:
            logging.error(f"生产者线程错误: {str(e)}")
            self.stop_event.set()
            raise
        finally:
            # 为每个消费者线程添加结束标记
            for _ in range(self.max_workers - 1):
                self.data_queue.put(None)
            logging.info("生产者线程结束")

    def consumer(self):
        """消费者：处理加密和数据插入"""
        while not self.stop_event.is_set():
            try:
                item = self.data_queue.get(timeout=self.timeout)
                if item is None:
                    logging.info("消费者线程收到结束信号")
                    break
                    
                batch, last_id = item
                self.process_batch(batch)
                self.save_checkpoint(last_id)
                self.data_queue.task_done()
                
            except queue.Empty:
                logging.warning("消费者等待超时，检查是否需要继续...")
                continue
            except Exception as e:
                logging.error(f"消费者线程错误: {str(e)}")
                self.stop_event.set()
                raise

    def run(self):
        """运行多线程加密处理"""
        start_time = datetime.now()
        total_processed = 0

        try:
            remote_conn = self.remote_pool.connection()
            
            # 创建线程池
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 启动生产者线程
                producer_future = executor.submit(self.producer, remote_conn)
                
                # 启动消费者线程
                consumer_futures = []
                for i in range(self.max_workers - 1):  # 预留一个线程给生产者
                    consumer_futures.append(executor.submit(self.consumer))
                
                # 等待所有线程完成，添加超时机制
                try:
                    producer_future.result(timeout=300)  # 5分钟超时
                    for future in consumer_futures:
                        future.result(timeout=300)  # 5分钟超时
                except TimeoutError:
                    logging.error("线程执行超时，正在强制停止...")
                    self.stop_event.set()
                    raise

        except Exception as e:
            logging.error(f"处理过程中出错: {str(e)}")
            self.stop_event.set()
            raise
        finally:
            remote_conn.close()

        end_time = datetime.now()
        duration = end_time - start_time
        logging.info(f"加密处理完成. 耗时: {duration}")

    def process_batch(self, batch_data: List[Dict]):
        """处理一批数据"""
        if not batch_data:
            return

        # 使用线程池并行处理加密操作
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            encrypted_batch = list(executor.map(self.encrypt_data, batch_data))
        
        # 处理无效日期
        for row in encrypted_batch:
            for field, value in row.items():
                if isinstance(value, str) and value in self.invalid_dates:
                    row[field] = None

        # 准备批量插入
        fields = encrypted_batch[0].keys()
        placeholders = ', '.join(['%s'] * len(fields))
        # 使用 REPLACE INTO 替代 INSERT INTO
        insert_sql = f"REPLACE INTO {self.table_name} ({', '.join(fields)}) VALUES ({placeholders})"
        
        # 执行批量插入
        local_conn = self.local_pool.connection()
        try:
            with local_conn.cursor() as cursor:
                values = [[row[field] for field in fields] for row in encrypted_batch]
                cursor.executemany(insert_sql, values)
            local_conn.commit()
            logging.info(f"成功插入/更新 {len(batch_data)} 条记录")
        except Exception as e:
            local_conn.rollback()
            logging.error(f"批量插入失败: {str(e)}")
            raise
        finally:
            local_conn.close()

if __name__ == "__main__":
    try:
        encryptor = DataEncryptor(batch_size=10000)
        encryptor.run()
    except Exception as e:
        logging.error(f"程序执行失败: {str(e)}")
    else:
        logging.info("程序执行成功完成") 