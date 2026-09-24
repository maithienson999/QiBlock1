import urllib.request
import re

# Nguồn duy nhất: ABPVN Filter
URLS = "https://abpvn.com/filter/abpvn-i6PlHq.txt",
"https://adguardteam.github.io/HostlistsRegistry/assets/filter_16.txt"

domains = set()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

print(f"Đang tải dữ liệu từ: {URL}")
try:
    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode('utf-8', errors='ignore')
        
        for line in content.splitlines():
            line = line.strip()
            
            # Bỏ qua dòng trống, comment (!), và quy tắc ẩn Element (##, #@#)
            if not line or line.startswith('!') or '##' in line or '#@#' in line:
                continue
            
            # Trích xuất domain từ quy tắc dạng ||example.com^
            if line.startswith('||') and '^' in line:
                domain = line.replace('||', '').split('^')[0].strip()
                # Loại bỏ wildcard (*) và các chuỗi không phải domain hợp lệ
                if domain and '.' in domain and not domain.startswith('*'):
                    domains.add(domain)
                    
            # Trích xuất domain từ quy tắc dạng hosts (0.0.0.0 / 127.0.0.1)
            elif not line.startswith('|'):
                parts = line.split()
                if len(parts) >= 2 and parts[0] in ['0.0.0.0', '127.0.0.1']:
                    domain = parts[1].strip()
                    if domain and domain != 'localhost':
                        domains.add(domain)

    # Ghi ra file blocklist.txt chuẩn AdGuard Home
    with open("blocklist.txt", "w", encoding="utf-8") as f:
        f.write("! Title: ABPVN Clean DNS Blocklist\n")
        f.write(f"! Total domains: {len(domains)}\n\n")
        for domain in sorted(domains):
            f.write(f"||{domain}^\n")

    print(f"Thành công! Đã trích xuất {len(domains)} domain từ ABPVN.")

except Exception as e:
    print(f"Lỗi khi xử lý file: {e}")
