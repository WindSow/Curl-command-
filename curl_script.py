import subprocess
import socket
from urllib.parse import urlparse

def validate_url_and_port(url, port):
    if port == 80 and not url.startswith("http://"):
        return False, "请确保URL以http://开头。"
    elif port == 443 and not url.startswith("https://"):
        return False, "请确保URL以https://开头。"
    elif port not in (80, 443) and f":{port}" not in url:
        return False, f"请确保URL包含端口号:{port}。"
    return True, ""

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def execute_curl_command(url, domain, port, ip):
    if ip:
        # 如果端口是非标准端口，则不重复端口号
        if port in (80, 443):
            command = f"curl -Iv -k {url} --resolve {domain}:{port}:{ip}"
        else:
            command = f"curl -Iv -k {url} --resolve {domain}:{ip}"
    else:
        command = f"curl -Iv -k {url}"
    
    print(f"Executing command: {command}")
    
    # 执行curl命令并获取输出
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # 打印标准输出和错误输出
    print(result.stdout)
    print(result.stderr)

    # 检查HTTP状态码是否为5XX或连接失败
    if "HTTP/1.1 5" in result.stdout or "HTTP/2 5" in result.stdout or "Could not connect" in result.stderr:
        print("连接失败或HTTP状态码为5XX，正在进行TCP连接测试...")
        tcp_ping_test(ip if ip else domain, port)

def tcp_ping_test(address, port):
    try:
        print(f"正在尝试连接到 {address} 的端口 {port}...")
        with socket.create_connection((address, port), timeout=5):
            print(f"成功连接到 {address} 的端口 {port}")
    except socket.gaierror:
        print(f"无法解析地址: {address}. 请检查输入。")
    except (socket.timeout, ConnectionRefusedError):
        print(f"无法连接到 {address} 的端口 {port}. 连接超时或被拒绝。")
    except Exception as e:
        print(f"发生错误: {e}")

def main():
    url = input("请输入URL: ")
    port = int(input("请输入端口: "))
    ip = input("请输入IP（如果为空，请直接按回车）: ")

    domain = extract_domain(url)
    
    if not domain:
        print("无法从URL中提取域名，请检查输入。")
        return
    
    is_valid, error_message = validate_url_and_port(url, port)
    
    if not is_valid:
        print(error_message)
        return
    
    execute_curl_command(url, domain, port, ip)

if __name__ == "__main__":
    main()