"""
自动代码服务系统
功能：自动接收请求、生成代码、交付、收费
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
import http.server
import threading
import webbrowser


class AutoCodeService:
    """自动代码服务"""

    def __init__(self, port=8080):
        self.port = port
        self.orders = []
        self.products = {
            'excel-tool': {
                'name': 'Excel自动化工具',
                'price': 10,
                'file': 'office-tools.zip',
                'description': '批量合并、提取、去重、清洗、报表'
            },
            'file-rename': {
                'name': '批量文件重命名',
                'price': 10,
                'file': 'office-tools.zip',
                'description': '前缀、后缀、编号、替换、正则'
            },
            'wechat-analysis': {
                'name': '微信聊天分析',
                'price': 15,
                'file': 'office-tools.zip',
                'description': '统计、搜索、词频、导出'
            },
            'custom-script': {
                'name': '定制Python脚本',
                'price': 20,
                'file': None,
                'description': '根据需求定制开发'
            }
        }

    def generate_order_id(self):
        """生成订单号"""
        timestamp = str(time.time())
        return hashlib.md5(timestamp.encode()).hexdigest()[:8].upper()

    def create_order(self, product_id, contact):
        """创建订单"""
        if product_id not in self.products:
            return None

        product = self.products[product_id]
        order = {
            'id': self.generate_order_id(),
            'product': product['name'],
            'price': product['price'],
            'contact': contact,
            'status': 'pending',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file': product['file']
        }
        self.orders.append(order)
        return order

    def get_payment_info(self, order_id):
        """获取付款信息"""
        for order in self.orders:
            if order['id'] == order_id:
                return {
                    'order_id': order['id'],
                    'product': order['product'],
                    'price': order['price'],
                    'payment_methods': [
                        {'name': '微信支付', 'qr': '请扫码支付'},
                        {'name': '支付宝', 'qr': '请扫码支付'},
                        {'name': 'GitHub Sponsors', 'url': 'https://github.com/sponsors/HHS3188'}
                    ]
                }
        return None

    def confirm_payment(self, order_id):
        """确认付款"""
        for order in self.orders:
            if order['id'] == order_id:
                order['status'] = 'paid'
                return order
        return None

    def deliver_product(self, order_id):
        """交付产品"""
        for order in self.orders:
            if order['id'] == order_id and order['status'] == 'paid':
                order['status'] = 'delivered'
                return {
                    'order_id': order['id'],
                    'product': order['product'],
                    'file': order['file'],
                    'message': '感谢购买！请下载附件。'
                }
        return None

    def generate_sales_page(self):
        """生成销售页面"""
        html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python自动化工具 - 立即购买</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 40px; border-radius: 12px; text-align: center; margin-bottom: 20px; }
        .product-card { background: white; border-radius: 12px; padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .product-card h3 { color: #667eea; margin-bottom: 8px; }
        .product-card .price { font-size: 2em; color: #e74c3c; font-weight: bold; }
        .product-card .btn { display: inline-block; background: #667eea; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-top: 12px; }
        .product-card .btn:hover { background: #5a6fd6; }
        .payment { background: #f8f9fa; padding: 20px; border-radius: 12px; margin-top: 20px; }
        .order-form { background: white; padding: 24px; border-radius: 12px; margin-top: 20px; }
        .order-form input, .order-form select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; }
        .order-form button { background: #667eea; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; width: 100%; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛠️ Python自动化工具包</h1>
            <p>效率提升10倍，告别重复劳动</p>
        </div>

        <div class="product-card">
            <h3>📊 Excel自动化处理</h3>
            <p>批量合并、数据提取、去重清洗、生成报表</p>
            <div class="price">¥10</div>
            <a href="#order" class="btn">立即购买</a>
        </div>

        <div class="product-card">
            <h3>📁 批量文件重命名</h3>
            <p>前缀、后缀、自动编号、文本替换、正则替换</p>
            <div class="price">¥10</div>
            <a href="#order" class="btn">立即购买</a>
        </div>

        <div class="product-card">
            <h3>💬 微信聊天分析</h3>
            <p>聊天记录统计、关键词搜索、词频分析、导出</p>
            <div class="price">¥15</div>
            <a href="#order" class="btn">立即购买</a>
        </div>

        <div class="product-card">
            <h3>🔧 定制Python脚本</h3>
            <p>根据您的需求定制开发自动化脚本</p>
            <div class="price">¥20起</div>
            <a href="#order" class="btn">立即购买</a>
        </div>

        <div class="order-form" id="order">
            <h2>📝 下单购买</h2>
            <form id="orderForm">
                <select name="product" required>
                    <option value="">选择产品</option>
                    <option value="excel-tool">Excel自动化工具 - ¥10</option>
                    <option value="file-rename">批量文件重命名 - ¥10</option>
                    <option value="wechat-analysis">微信聊天分析 - ¥15</option>
                    <option value="custom-script">定制Python脚本 - ¥20起</option>
                </select>
                <input type="text" name="contact" placeholder="联系方式（微信/邮箱）" required>
                <input type="text" name="需求" placeholder="具体需求（可选）">
                <button type="submit">提交订单</button>
            </form>
        </div>

        <div class="payment">
            <h2>💳 付款方式</h2>
            <p>1. GitHub Sponsors: <a href="https://github.com/sponsors/HHS3188">点击赞助</a></p>
            <p>2. 微信/支付宝: 请添加微信联系</p>
            <p>3. 付款后请发送订单号确认</p>
        </div>
    </div>

    <script>
        document.getElementById('orderForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const product = formData.get('product');
            const contact = formData.get('contact');

            // 生成订单号
            const orderId = Math.random().toString(36).substr(2, 8).toUpperCase();

            alert(`订单已创建！\n\n订单号: ${orderId}\n产品: ${product}\n联系方式: ${contact}\n\n请付款后发送订单号确认。`);

            // 这里可以发送到服务器
            console.log('Order:', { orderId, product, contact });
        });
    </script>
</body>
</html>
"""
        return html

    def start_server(self):
        """启动服务器"""
        html = self.generate_sales_page()

        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())

                if 'action' in data:
                    if data['action'] == 'create_order':
                        order = self.create_order(data['product'], data['contact'])
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(order).encode())

        server = http.server.HTTPServer(('localhost', self.port), Handler)
        print(f"🚀 服务已启动: http://localhost:{self.port}")
        print(f"📋 产品列表:")
        for pid, product in self.products.items():
            print(f"  - {product['name']}: ¥{product['price']}")
        print(f"\n💡 请在浏览器中打开上述地址")

        # 自动打开浏览器
        webbrowser.open(f'http://localhost:{self.port}')

        server.serve_forever()


def main():
    service = AutoCodeService()
    print("="*50)
    print("  🛠️ Python自动化工具 - 自动销售系统")
    print("="*50)
    print()
    print("📦 可用产品:")
    for pid, product in service.products.items():
        print(f"  [{pid}] {product['name']} - ¥{product['price']}")
        print(f"       {product['description']}")
    print()
    print("🚀 启动销售服务器...")
    print()

    try:
        service.start_server()
    except KeyboardInterrupt:
        print("\n⏹️ 服务器已停止")


if __name__ == '__main__':
    main()
