import pymysql
from pymysql.cursors import DictCursor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from dotenv import load_dotenv
import pandas as pd
import logging
from datetime import datetime
from dbutils.pooled_db import PooledDB
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import queue
from threading import Event
import base64


class DataDecryptor:
    def __init__(self, 
                 fields_to_decrypt=None,
                 table_name='solid_order_main_wrong',
                 batch_size=10000,
                 output_file=None
                 ):
        """
        初始化解密器
        
        Args:
            fields_to_decrypt (list): 需要解密的字段列表
            table_name (str): 要处理的表名
            batch_size (int): 每批处理的记录数
            output_file (str): 输出的Excel文件名
        """
        # 加载环境变量
        load_dotenv()
        
        # 设置解密字段
        self.fields_to_decrypt = fields_to_decrypt or ['dirver_phone', 'trans_number']
        self.table_name = table_name
        self.batch_size = batch_size
        self.output_file = output_file or f'decrypted_data_{datetime.now().strftime("%Y%m%d")}.xlsx'
        
        # 初始化解密器和数据库连接
        self.setup_decryption()
        self.setup_database_pool()
        self.max_workers = 4  # 工作线程数
        self.data_queue = queue.Queue(maxsize=10)
        self.stop_event = Event()

    def setup_decryption(self):
        """设置解密器"""
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("未找到加密密钥")
        
        # 确保密钥是32字节
        key_bytes = base64.urlsafe_b64decode(key.encode())
        if len(key_bytes) != 32:
            raise ValueError("密钥必须是32字节(256位)")
            
        # 使用固定的IV
        self.iv = b'\x00' * 16
        self.key = key_bytes

    def setup_database_pool(self):
        """设置数据库连接池"""
        self.db_pool = PooledDB(
            creator=pymysql,
            maxconnections=5,
            host=os.getenv('local_host'),
            user=os.getenv('local_user'),
            password=os.getenv('local_password'),
            database=os.getenv('local_database'),
            cursorclass=DictCursor
        )

    def decrypt_value(self, value: str) -> str:
        """解密单个值"""
        if not value:
            return value
            
        try:
            cipher = Cipher(
                algorithms.AES(self.key),
                modes.CBC(self.iv),
                backend=default_backend()
            )
            
            encrypted_data = base64.urlsafe_b64decode(value.encode())
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            data = unpadder.update(padded_data) + unpadder.finalize()
            
            return data.decode()
            
        except Exception as e:
            logging.error(f"解密值失败: {str(e)}")
            return None

    def decrypt_batch(self, batch_data: List[Dict]) -> List[Dict]:
        """解密一批数据"""
        decrypted_batch = []
        for row in batch_data:
            decrypted_row = row.copy()
            for field in self.fields_to_decrypt:
                if field in row and row[field]:
                    decrypted_row[field] = self.decrypt_value(row[field])
            decrypted_batch.append(decrypted_row)
        return decrypted_batch

    def producer(self, cursor):
        """生产者：读取数据"""
        offset = 0
        try:
            while not self.stop_event.is_set() and offset < self.total_records:
                cursor.execute(
                    f"SELECT * FROM {self.table_name} LIMIT %s OFFSET %s",
                    (self.batch_size, offset)
                )
                batch = cursor.fetchall()
                if not batch:
                    break
                
                self.data_queue.put(batch)
                offset += len(batch)
                
        finally:
            # 发送结束信号
            for _ in range(self.max_workers):
                self.data_queue.put(None)

    def consumer(self, result_queue):
        """消费者：解密数据"""
        while not self.stop_event.is_set():
            try:
                batch = self.data_queue.get(timeout=30)
                if batch is None:
                    break
                    
                decrypted_batch = self.decrypt_batch(batch)
                result_queue.put(decrypted_batch)
                self.data_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"解密错误: {str(e)}")
                self.stop_event.set()
                raise

    def process_and_save(self):
        """处理数据并保存到Excel"""
        try:
            conn = self.db_pool.connection()
            all_data = []
            total_processed = 0
            
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) as count FROM {self.table_name}")
                total_records = cursor.fetchone()['count']
                logging.info(f"开始处理总记录数: {total_records}")

                offset = 0
                while offset < total_records:
                    cursor.execute(
                        f"SELECT * FROM {self.table_name} LIMIT %s OFFSET %s",
                        (self.batch_size, offset)
                    )
                    batch = cursor.fetchall()
                    if not batch:
                        break

                    decrypted_batch = self.decrypt_batch(batch)
                    all_data.extend(decrypted_batch)
                    
                    total_processed += len(batch)
                    offset += self.batch_size
                    if total_processed % 50000 == 0:  # 每50000条记录输出一次进度
                        logging.info(f"已处理: {total_processed}/{total_records} 条记录")

            df = pd.DataFrame(all_data)
            with pd.ExcelWriter(self.output_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Decrypted_Data')
                
            logging.info(f"数据已保存到: {self.output_file}")
            
        except Exception as e:
            logging.error(f"处理过程中出错: {str(e)}")
            raise
        finally:
            conn.close()

if __name__ == "__main__":
    try:
        decryptor = DataDecryptor(
            fields_to_decrypt=['dirver_phone', 'trans_number'],
            table_name='solid_order_main_wrong',
            batch_size=10000,
            output_file='decrypted_data.xlsx'
        )
        decryptor.process_and_save()
    except Exception as e:
        logging.error(f"程序执行失败: {str(e)}")
    else:
        logging.info("程序执行成功完成") 