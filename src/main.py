# 帮我整合download.py和upload.py到一起
# 参数解析
import argparse
import configparser
import logging
import os
from download import download_from_aliyun
from upload import upload_to_aliyun

# 设置日志记录
logging.basicConfig(filename="../app.log", level=logging.INFO)

def check_config(required_params):
    """
    检查配置文件中是否包含了所有必需的参数。
    
    :param required_params: 一个列表，包含了所有必需的参数名称。
    :raises ValueError: 如果配置文件中缺少某个必需的参数，则抛出此异常。
    """
    for param in required_params:
        # 如果配置文件中不存在当前参数，则抛出ValueError异常
        if not config.has_option('AliPCSDownload', param):
            raise ValueError(f"Missing required parameter: {param}")
        

if __name__ == '__main__':

    # 构建配置文件的完整路径
    script_dir = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(script_dir, '..', 'config.ini')

    # 读取参数
    parser = argparse.ArgumentParser(description='Aliyun backup tool')
    parser.add_argument('--action', type=str, default='download', choices=['download', 'upload'], help='download or upload')
    parser.add_argument('--file', type=str, default=config_file_path, help='config file path')
    args = parser.parse_args()

    # 读取配置文件
    config = configparser.ConfigParser(interpolation=None)
    config.read(args.file)
    remote_path = config.get('AliPCSDownload', 'remote_path')
    local_path = config.get('AliPCSDownload', 'local_path')
    download_path = config.get('AliPCSDownload', 'download_path', fallback=None)
    refresh_token = config.get('AliPCSDownload', 'refresh_token')
    encrypt_password = config.get('AliPCSDownload', 'encrypt_password', fallback=None)
    if encrypt_password is not None:
        encrypt_password = encrypt_password.encode("utf-8")

    if args.action == 'download':
        required_params = ['remote_path', 'download_path', 'refresh_token']
        check_config(required_params)
        download_from_aliyun(remote_path, download_path, refresh_token, encrypt_password)
    elif args.action == 'upload':
        required_params = ['remote_path', 'local_path', 'refresh_token']
        check_config(required_params)
        upload_to_aliyun(local_path, remote_path, refresh_token, encrypt_password)
    else:
        logging.info('argument error')

