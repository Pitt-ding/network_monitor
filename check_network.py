import datetime
import subprocess
import re
import argparse
import sys


# -----1 test network
def check_network(ip_address: str,
                  file_path: str = r'C:\Users\reedi\Desktop\Python_code\project\network_monitor\network_mon.csv') -> None:
    _cmd = f'ping {ip_address} -t'
    _match_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    _match_bytes = re.compile(r'\s..=(\d+)\s')
    _match_time = re.compile(r'.\d+ms')
    _match_ttl = re.compile(r'TTL=(\d+)')
    _subprocess = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)
    try:
        while True:
            try:
                line = _subprocess.stdout.readline()
                if not line:
                    break
                else:
                    _ip_str = _match_ip.search(line)
                    _bytes_str = _match_bytes.search(line)
                    _time_str = _match_time.search(line)
                    _ttl_str = _match_ttl.search(line)
                    if _ip_str and _bytes_str and _time_str and _ttl_str:
                        _str_list = map(str, [datetime.datetime.now(), _ip_str.group(), _bytes_str.group(1),
                                              _time_str.group(), _ttl_str.group(1)])
                        _csv_str = ','.join(_str_list)
                        print(f'{datetime.datetime.now()}: {line.strip()}')
                        write_to_file(_csv_str, file_path)
            except PermissionError:
                print(f'PermissionError: can not write to file {file_path}')
            except Exception as e:
                print(f'Error: {e}')

    finally:
        _subprocess.stdout.close()
        _subprocess.stderr.close()
        _subprocess.wait()


# -----2 write result to file
def write_to_file(content: str, file_name: str = 'check_network_log.csv') -> None:
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f'{content}\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(f'run check_network function with command line arguments')
        parser = argparse.ArgumentParser(description='Check network connectivity by pinging a specified IP address.')
        parser.add_argument('ip_address', type=str, help='The IP address to ping.')
        parser.add_argument('file_path', type=str, help='The path to the log file.')
        args = parser.parse_args()
        check_network(args.ip_address, args.file_path)
    else:
        print(f'run check_network function with default parameters')
        check_network('192.168.0.10', r'C:\Users\reedi\Desktop\Python_code\project\network_monitor\network_mon.csv')
