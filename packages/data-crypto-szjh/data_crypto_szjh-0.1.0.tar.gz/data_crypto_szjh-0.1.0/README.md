# Data Crypto

一个用于数据加密和解密的Python工具包，主要用于处理数据库中的敏感信息。

## 功能特点

- 支持AES-256-CBC加密/解密
- 支持批量数据处理
- 支持数据库连接池
- 支持导出解密后的数据到Excel
- 多线程处理提升性能
- 支持断点续传
- 支持无效日期处理

## 安装

```bash
pip install data-crypto
```

## 环境变量配置

在使用前需要配置以下环境变量，可以创建 `.env` 文件：

### 本地数据库配置
```.env
local_host=本地数据库地址
local_user=本地数据库用户名
local_password=本地数据库密码
local_database=本地数据库名
```

### 远程数据库配置
```.env
remote_host=远程数据库地址
remote_user=远程数据库用户名
remote_password=远程数据库密码
remote_database=远程数据库名
```

### 加密密钥配置（也可以不配置，系统会随机生成一个）
```.env
ENCRYPTION_KEY=your_encryption_key
```


## 使用示例

### DataEncryptor 类

DataEncryptor 类用于加密数据库中的敏感字段。

#### 参数说明：
- `fields_to_encrypt`: 需要加密的字段列表
- `batch_size`: 每批处理的记录数（默认1000）
- `table_name`: 要处理的表名
- `max_workers`: 工作线程数（默认4）
- `queue_size`: 队列大小（默认10）
- `checkpoint_file`: 断点续传文件路径
- `timeout`: 队列等待超时时间（秒）
- `invalid_dates`: 需要处理的无效日期列表

```python
from data_crypto import encryptor

encryptor = encryptor.DataEncryptor()
encryptor.run()
```

### DataDecryptor 类

DataDecryptor 类用于解密数据库中的加密字段并导出到Excel文件。

#### 参数说明：
- `fields_to_decrypt`: 需要解密的字段列表
- `table_name`: 要处理的数据表名
- `batch_size`: 每批处理的记录数
- `output_file`: 输出的Excel文件名

```python
from data_crypto import decryptor

decryptor = decryptor.DataDecryptor()
decryptor.run()
```
