"""
Python 自动化工具 API
功能：提供在线代码生成服务
"""

import json
import hashlib
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import webbrowser


class CodeServiceAPI(BaseHTTPRequestHandler):
    """代码服务 API"""

    def do_GET(self):
        """处理 GET 请求"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == '/' or path == '/index.html':
            self.serve_homepage()
        elif path == '/api/products':
            self.serve_products()
        elif path == '/api/generate':
            self.generate_code(params)
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """处理 POST 请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())

        if self.path == '/api/order':
            self.create_order(data)
        else:
            self.send_error(404, "Not Found")

    def serve_homepage(self):
        """提供主页"""
        html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python 自动化工具 - 在线代码生成服务</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 40px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
        .header h1 { font-size: 2em; margin-bottom: 10px; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .feature { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .feature h3 { color: #667eea; margin-bottom: 12px; }
        .pricing { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .pricing h2 { color: #667eea; margin-bottom: 16px; }
        .price-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
        .price-card { border: 2px solid #667eea; border-radius: 12px; padding: 20px; text-align: center; }
        .price-card.popular { background: #667eea; color: white; }
        .price-card h3 { margin-bottom: 8px; }
        .price-card .price { font-size: 2em; font-weight: bold; margin-bottom: 12px; }
        .price-card .btn { display: inline-block; background: #667eea; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; }
        .price-card.popular .btn { background: white; color: #667eea; }
        .generator { background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .generator h2 { color: #667eea; margin-bottom: 16px; }
        .generator select, .generator input, .generator textarea { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; }
        .generator button { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; width: 100%; }
        .generator button:hover { background: #5a6fd6; }
        .result { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 16px; white-space: pre-wrap; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛠️ Python 自动化工具</h1>
            <p>在线代码生成服务 - 效率提升10倍</p>
        </div>

        <div class="features">
            <div class="feature">
                <h3>📊 Excel 自动化</h3>
                <p>批量合并、数据提取、去重清洗、生成报表</p>
            </div>
            <div class="feature">
                <h3>📁 文件重命名</h3>
                <p>前缀、后缀、自动编号、正则替换</p>
            </div>
            <div class="feature">
                <h3>💬 微信分析</h3>
                <p>聊天记录统计、关键词搜索、词频分析</p>
            </div>
            <div class="feature">
                <h3>🔧 定制开发</h3>
                <p>根据需求定制 Python 自动化脚本</p>
            </div>
        </div>

        <div class="pricing">
            <h2>💰 价格方案</h2>
            <div class="price-cards">
                <div class="price-card">
                    <h3>基础版</h3>
                    <div class="price">¥10</div>
                    <p>1个工具</p>
                    <a href="#generator" class="btn">立即购买</a>
                </div>
                <div class="price-card popular">
                    <h3>标准版</h3>
                    <div class="price">¥20</div>
                    <p>3个工具</p>
                    <a href="#generator" class="btn">立即购买</a>
                </div>
                <div class="price-card">
                    <h3>高级版</h3>
                    <div class="price">¥30</div>
                    <p>全部工具 + 定制</p>
                    <a href="#generator" class="btn">立即购买</a>
                </div>
            </div>
        </div>

        <div class="generator" id="generator">
            <h2>🎮 在线代码生成器</h2>
            <select id="toolType">
                <option value="">选择工具类型</option>
                <option value="excel-merge">Excel 合并</option>
                <option value="excel-extract">Excel 提取</option>
                <option value="file-rename">文件重命名</option>
                <option value="wechat-analysis">微信分析</option>
            </select>
            <input type="text" id="requirements" placeholder="具体需求描述">
            <button onclick="generateCode()">生成代码</button>
            <div id="result" class="result" style="display:none;"></div>
        </div>
    </div>

    <script>
        async function generateCode() {
            const toolType = document.getElementById('toolType').value;
            const requirements = document.getElementById('requirements').value;

            if (!toolType) {
                alert('请选择工具类型');
                return;
            }

            const response = await fetch('/api/generate?type=' + toolType + '&req=' + encodeURIComponent(requirements));
            const data = await response.json();

            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.textContent = data.code;
        }
    </script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def serve_products(self):
        """提供产品列表"""
        products = [
            {'id': 'excel-tool', 'name': 'Excel自动化工具', 'price': 10},
            {'id': 'file-rename', 'name': '批量文件重命名', 'price': 10},
            {'id': 'wechat-analysis', 'name': '微信聊天分析', 'price': 15},
            {'id': 'custom-script', 'name': '定制Python脚本', 'price': 20}
        ]
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(products).encode())

    def generate_code(self, params):
        """生成代码"""
        tool_type = params.get('type', [''])[0]
        requirements = params.get('req', [''])[0]

        code_templates = {
            'excel-merge': '''
import pandas as pd
from pathlib import Path

def merge_excel_files(input_dir, output_file="merged.xlsx"):
    """合并目录下所有Excel文件"""
    files = list(Path(input_dir).glob("*.xlsx"))
    all_data = []
    for file in files:
        df = pd.read_excel(file)
        df['_来源'] = file.name
        all_data.append(df)
    merged = pd.concat(all_data, ignore_index=True)
    merged.to_excel(output_file, index=False)
    print(f"✅ 合并完成: {output_file}")
    return merged

# 使用方法
merge_excel_files("你的Excel文件夹")
''',
            'excel-extract': '''
import pandas as pd

def extract_columns(input_file, columns, output_file="extracted.xlsx"):
    """提取指定列"""
    df = pd.read_excel(input_file)
    extracted = df[columns]
    extracted.to_excel(output_file, index=False)
    print(f"✅ 提取完成: {output_file}")
    return extracted

# 使用方法
extract_columns("data.xlsx", ["姓名", "年龄", "邮箱"])
''',
            'file-rename': '''
import os
from pathlib import Path

def batch_rename(directory, prefix="", suffix=""):
    """批量重命名文件"""
    for i, file in enumerate(Path(directory).iterdir(), 1):
        if file.is_file():
            new_name = f"{prefix}{file.stem}{suffix}{file.suffix}"
            file.rename(file.parent / new_name)
            print(f"{file.name} -> {new_name}")

# 使用方法
batch_rename("你的文件夹", prefix="备份_")
''',
            'wechat-analysis': '''
import re
from collections import Counter

def analyze_chat(file_path):
    """分析微信聊天记录"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 统计发言次数
    senders = re.findall(r'\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2} (.+?)$', content, re.MULTILINE)
    sender_count = Counter(senders)

    print("📊 发言统计:")
    for sender, count in sender_count.most_common(10):
        print(f"  {sender}: {count}条")

    return sender_count

# 使用方法
analyze_chat("chat.txt")
'''
        }

        code = code_templates.get(tool_type, "# 未知工具类型")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'code': code}).encode())

    def create_order(self, data):
        """创建订单"""
        order_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8].upper()
        order = {
            'id': order_id,
            'product': data.get('product', ''),
            'price': data.get('price', 0),
            'contact': data.get('contact', ''),
            'status': 'pending'
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(order).encode())


def main():
    port = 8080
    server = HTTPServer(('localhost', port), CodeServiceAPI)
    print(f"🚀 服务已启动: http://localhost:{port}")
    print(f"📋 API 端点:")
    print(f"  - GET  /             # 主页")
    print(f"  - GET  /api/products # 产品列表")
    print(f"  - GET  /api/generate # 生成代码")
    print(f"  - POST /api/order    # 创建订单")
    print(f"\n💡 请在浏览器中打开上述地址")

    webbrowser.open(f'http://localhost:{port}')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")


if __name__ == '__main__':
    main()
