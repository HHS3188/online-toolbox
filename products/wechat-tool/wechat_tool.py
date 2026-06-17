"""
微信聊天记录导出与分析工具
功能：导出微信聊天记录、统计分析、关键词搜索、生成报告
"""

import os
import re
import json
import csv
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path
import argparse


class WechatAnalyzer:
    """微信聊天记录分析工具"""

    def __init__(self, data_path=None):
        self.messages = []
        self.data_path = data_path

    def load_from_txt(self, filepath):
        """从TXT文件加载聊天记录"""
        patterns = [
            # 格式: 2024-01-01 12:00:00 张三
            r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)$',
            # 格式: 2024/1/1 12:00 张三
            r'^(\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{2})\s+(.+?)$',
            # 格式: [2024-01-01 12:00:00] 张三:
            r'^\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]\s+(.+?):',
        ]

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_msg = None
        for line in lines:
            line = line.strip()
            if not line:
                continue

            matched = False
            for pattern in patterns:
                match = re.match(pattern, line)
                if match:
                    if current_msg:
                        self.messages.append(current_msg)
                    time_str, sender = match.groups()
                    content = line[match.end():].strip()
                    current_msg = {
                        'time': time_str,
                        'sender': sender,
                        'content': content
                    }
                    matched = True
                    break

            if not matched and current_msg:
                current_msg['content'] += '\n' + line

        if current_msg:
            self.messages.append(current_msg)

        print(f"✅ 加载完成: {len(self.messages)} 条消息")
        return len(self.messages)

    def load_from_csv(self, filepath):
        """从CSV文件加载聊天记录"""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.messages.append({
                    'time': row.get('time', ''),
                    'sender': row.get('sender', ''),
                    'content': row.get('content', '')
                })
        print(f"✅ 加载完成: {len(self.messages)} 条消息")
        return len(self.messages)

    def load_from_json(self, filepath):
        """从JSON文件加载聊天记录"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.messages = json.load(f)
        print(f"✅ 加载完成: {len(self.messages)} 条消息")
        return len(self.messages)

    def search(self, keyword, case_sensitive=False):
        """搜索关键词"""
        results = []
        for msg in self.messages:
            content = msg['content']
            if not case_sensitive:
                content = content.lower()
                keyword = keyword.lower()
            if keyword in content:
                results.append(msg)
        print(f"🔍 找到 {len(results)} 条包含 '{keyword}' 的消息")
        return results

    def search_regex(self, pattern):
        """正则表达式搜索"""
        results = []
        regex = re.compile(pattern)
        for msg in self.messages:
            if regex.search(msg['content']):
                results.append(msg)
        print(f"🔍 正则匹配到 {len(results)} 条消息")
        return results

    def get_statistics(self):
        """获取统计信息"""
        if not self.messages:
            print("❌ 没有加载数据")
            return None

        stats = {
            'total_messages': len(self.messages),
            'unique_senders': len(set(m['sender'] for m in self.messages)),
            'senders': Counter(m['sender'] for m in self.messages),
            'date_range': {
                'start': min(m['time'] for m in self.messages),
                'end': max(m['time'] for m in self.messages)
            },
            'avg_message_length': sum(len(m['content']) for m in self.messages) / len(self.messages),
            'total_chars': sum(len(m['content']) for m in self.messages)
        }

        # 按日期统计
        daily = defaultdict(int)
        for msg in self.messages:
            date = msg['time'][:10]
            daily[date] += 1
        stats['daily_counts'] = dict(sorted(daily.items()))

        # 按小时统计
        hourly = defaultdict(int)
        for msg in self.messages:
            try:
                hour = msg['time'][11:13]
                hourly[hour] += 1
            except:
                pass
        stats['hourly_counts'] = dict(sorted(hourly.items()))

        return stats

    def print_statistics(self):
        """打印统计信息"""
        stats = self.get_statistics()
        if not stats:
            return

        print("\n" + "="*50)
        print("📊 聊天记录统计报告")
        print("="*50)

        print(f"\n📈 基本统计:")
        print(f"  总消息数: {stats['total_messages']}")
        print(f"  参与人数: {stats['unique_senders']}")
        print(f"  总字符数: {stats['total_chars']}")
        print(f"  平均消息长度: {stats['avg_message_length']:.1f} 字符")
        print(f"  时间范围: {stats['date_range']['start']} ~ {stats['date_range']['end']}")

        print(f"\n👥 发言排行:")
        for sender, count in stats['senders'].most_common(10):
            percentage = count / stats['total_messages'] * 100
            print(f"  {sender}: {count} 条 ({percentage:.1f}%)")

        print(f"\n📅 每日消息数 (前10天):")
        for date, count in list(stats['daily_counts'].items())[:10]:
            print(f"  {date}: {count} 条")

        print(f"\n⏰ 按小时分布:")
        for hour, count in sorted(stats['hourly_counts'].items()):
            bar = '█' * (count // 10)
            print(f"  {hour}:00 - {count} 条 {bar}")

        return stats

    def find_links(self):
        """查找所有链接"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        links = []
        for msg in self.messages:
            found = re.findall(url_pattern, msg['content'])
            for url in found:
                links.append({
                    'url': url,
                    'sender': msg['sender'],
                    'time': msg['time']
                })
        print(f"🔗 找到 {len(links)} 个链接")
        return links

    def find_images(self):
        """查找图片消息"""
        image_keywords = ['[图片]', '[表情]', '[Photo]', '[Image]']
        images = []
        for msg in self.messages:
            for keyword in image_keywords:
                if keyword in msg['content']:
                    images.append(msg)
                    break
        print(f"🖼️ 找到 {len(images)} 条图片消息")
        return images

    def find_red_packets(self):
        """查找红包消息"""
        packet_keywords = ['[红包]', '[微信红包]', '红包', '转账']
        packets = []
        for msg in self.messages:
            for keyword in packet_keywords:
                if keyword in msg['content']:
                    packets.append(msg)
                    break
        print(f"🧧 找到 {len(packets)} 条红包/转账消息")
        return packets

    def word_frequency(self, top_n=20, exclude_common=True):
        """词频统计"""
        common_words = {'的', '了', '是', '我', '你', '他', '她', '它', '在', '有',
                       '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很',
                       '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
                       '自己', '这', '他', '她', '吗', '吧', '啊', '呢', '嗯', '哦'}

        words = []
        for msg in self.messages:
            # 简单分词（按标点和空格）
            content = msg['content']
            # 移除表情和特殊字符
            content = re.sub(r'\[.*?\]', '', content)
            content = re.sub(r'[^\w一-鿿]', ' ', content)
            # 分割
            for word in content.split():
                if len(word) >= 2:
                    if not exclude_common or word not in common_words:
                        words.append(word)

        freq = Counter(words)
        print(f"\n📝 词频统计 (前{top_n}):")
        for word, count in freq.most_common(top_n):
            print(f"  {word}: {count}")

        return freq

    def export_to_txt(self, output_file="chat_export.txt"):
        """导出为TXT文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for msg in self.messages:
                f.write(f"{msg['time']} {msg['sender']}\n{msg['content']}\n\n")
        print(f"✅ 导出完成: {output_file}")

    def export_to_csv(self, output_file="chat_export.csv"):
        """导出为CSV文件"""
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['time', 'sender', 'content'])
            writer.writeheader()
            writer.writerows(self.messages)
        print(f"✅ 导出完成: {output_file}")

    def export_to_json(self, output_file="chat_export.json"):
        """导出为JSON文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
        print(f"✅ 导出完成: {output_file}")

    def generate_report(self, output_file="chat_report.txt"):
        """生成完整分析报告"""
        stats = self.get_statistics()
        if not stats:
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("微信聊天记录分析报告\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*60 + "\n\n")

            f.write("【基本信息】\n")
            f.write(f"总消息数: {stats['total_messages']}\n")
            f.write(f"参与人数: {stats['unique_senders']}\n")
            f.write(f"总字符数: {stats['total_chars']}\n")
            f.write(f"平均消息长度: {stats['avg_message_length']:.1f} 字符\n")
            f.write(f"时间范围: {stats['date_range']['start']} ~ {stats['date_range']['end']}\n\n")

            f.write("【发言排行】\n")
            for sender, count in stats['senders'].most_common():
                percentage = count / stats['total_messages'] * 100
                f.write(f"  {sender}: {count} 条 ({percentage:.1f}%)\n")

            f.write("\n【每日消息数】\n")
            for date, count in stats['daily_counts'].items():
                f.write(f"  {date}: {count} 条\n")

            f.write("\n【按小时分布】\n")
            for hour, count in stats['hourly_counts'].items():
                f.write(f"  {hour}:00 - {count} 条\n")

            f.write("\n" + "="*60 + "\n")

        print(f"✅ 报告生成完成: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='微信聊天记录分析工具')
    parser.add_argument('action', choices=['analyze', 'search', 'export', 'report'],
                       help='操作类型')
    parser.add_argument('-i', '--input', required=True, help='输入文件')
    parser.add_argument('-o', '--output', help='输出文件')
    parser.add_argument('-k', '--keyword', help='搜索关键词')
    parser.add_argument('-r', '--regex', help='正则表达式')
    parser.add_argument('-f', '--format', choices=['txt', 'csv', 'json'], default='txt',
                       help='导出格式')

    args = parser.parse_args()
    analyzer = WechatAnalyzer()

    # 加载数据
    if args.input.endswith('.csv'):
        analyzer.load_from_csv(args.input)
    elif args.input.endswith('.json'):
        analyzer.load_from_json(args.input)
    else:
        analyzer.load_from_txt(args.input)

    # 执行操作
    if args.action == 'analyze':
        analyzer.print_statistics()
        analyzer.word_frequency()
        links = analyzer.find_links()
        if links:
            print(f"\n🔗 链接列表:")
            for link in links[:10]:
                print(f"  {link['time']} {link['sender']}: {link['url']}")

    elif args.action == 'search':
        if args.keyword:
            results = analyzer.search(args.keyword)
        elif args.regex:
            results = analyzer.search_regex(args.regex)
        else:
            print("❌ 请指定 -k 或 -r 参数")
            return

        output = args.output or 'search_results.txt'
        with open(output, 'w', encoding='utf-8') as f:
            for msg in results:
                f.write(f"{msg['time']} {msg['sender']}\n{msg['content']}\n\n")
        print(f"✅ 搜索结果已保存: {output}")

    elif args.action == 'export':
        output = args.output or f'chat_export.{args.format}'
        if args.format == 'csv':
            analyzer.export_to_csv(output)
        elif args.format == 'json':
            analyzer.export_to_json(output)
        else:
            analyzer.export_to_txt(output)

    elif args.action == 'report':
        output = args.output or 'chat_report.txt'
        analyzer.generate_report(output)


if __name__ == '__main__':
    main()
