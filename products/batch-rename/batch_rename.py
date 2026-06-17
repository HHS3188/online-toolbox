"""
批量文件重命名工具
功能：按规则批量重命名文件，支持正则、序号、日期等
"""

import os
import re
import argparse
from pathlib import Path
from datetime import datetime


class BatchRenamer:
    """批量文件重命名工具"""

    def __init__(self, directory):
        self.dir = Path(directory)
        if not self.dir.exists():
            raise FileNotFoundError(f"目录不存在: {directory}")

    def list_files(self, pattern="*"):
        """列出匹配的文件"""
        files = list(self.dir.glob(pattern))
        files = [f for f in files if f.is_file()]
        return sorted(files)

    def add_prefix(self, prefix, pattern="*"):
        """添加前缀"""
        files = self.list_files(pattern)
        print(f"📁 找到 {len(files)} 个文件")

        for i, file in enumerate(files, 1):
            new_name = file.parent / f"{prefix}{file.name}"
            file.rename(new_name)
            print(f"  {i}. {file.name} → {new_name.name}")

        print(f"✅ 完成，共重命名 {len(files)} 个文件")

    def add_suffix(self, suffix, pattern="*"):
        """添加后缀（在扩展名之前）"""
        files = self.list_files(pattern)
        print(f"📁 找到 {len(files)} 个文件")

        for i, file in enumerate(files, 1):
            new_name = file.parent / f"{file.stem}{suffix}{file.suffix}"
            file.rename(new_name)
            print(f"  {i}. {file.name} → {new_name.name}")

        print(f"✅ 完成，共重命名 {len(files)} 个文件")

    def add_number(self, start=1, step=1, pattern="*"):
        """添加序号"""
        files = self.list_files(pattern)
        print(f"📁 找到 {len(files)} 个文件")

        digits = len(str(start + len(files) - 1))
        for i, file in enumerate(files):
            num = start + i * step
            new_name = file.parent / f"{str(num).zfill(digits)}_{file.name}"
            file.rename(new_name)
            print(f"  {i+1}. {file.name} → {new_name.name}")

        print(f"✅ 完成，共重命名 {len(files)} 个文件")

    def replace_text(self, old_text, new_text, pattern="*"):
        """替换文件名中的文本"""
        files = self.list_files(pattern)
        print(f"📁 找到 {len(files)} 个文件")

        count = 0
        for file in files:
            if old_text in file.stem:
                new_name = file.parent / file.name.replace(old_text, new_text)
                file.rename(new_name)
                print(f"  {file.name} → {new_name.name}")
                count += 1

        print(f"✅ 完成，共重命名 {count} 个文件")

    def regex_replace(self, pattern_str, replacement, pattern="*"):
        """使用正则表达式替换"""
        files = self.list_files(pattern)
        print(f"📁 找到 {len(files)} 个文件")

        count = 0
        for file in files:
            new_stem = re.sub(pattern_str, replacement, file.stem)
            if new_stem != file.stem:
                new_name = file.parent / f"{new_stem}{file.suffix}"
                file.rename(new_name)
                print(f"  {file.name} → {new_name.name}")
                count += 1

        print(f"✅ 完成，共重命名 {count} 个文件")

    def change_case(self, case_type, pattern="*"):
        """修改大小写"""
        files = self.list_files(pattern)
        print(f"📁 找到 {len(files)} 个文件")

        for file in files:
            if case_type == 'upper':
                new_stem = file.stem.upper()
            elif case_type == 'lower':
                new_stem = file.stem.lower()
            elif case_type == 'title':
                new_stem = file.stem.title()
            else:
                continue

            if new_stem != file.stem:
                new_name = file.parent / f"{new_stem}{file.suffix}"
                file.rename(new_name)
                print(f"  {file.name} → {new_name.name}")

        print(f"✅ 完成")

    def add_date(self, date_format="%Y%m%d", pattern="*"):
        """添加日期前缀"""
        files = self.list_files(pattern)
        today = datetime.now().strftime(date_format)
        print(f"📁 找到 {len(files)} 个文件")

        for i, file in enumerate(files, 1):
            new_name = file.parent / f"{today}_{file.name}"
            file.rename(new_name)
            print(f"  {i}. {file.name} → {new_name.name}")

        print(f"✅ 完成，共重命名 {len(files)} 个文件")

    def preview(self, action, **kwargs):
        """预览重命名结果（不实际执行）"""
        files = self.list_files(kwargs.get('pattern', '*'))
        print(f"📁 找到 {len(files)} 个文件")
        print("\n📋 预览:")
        for i, file in enumerate(files, 1):
            if action == 'prefix':
                new_name = f"{kwargs['prefix']}{file.name}"
            elif action == 'suffix':
                new_name = f"{file.stem}{kwargs['suffix']}{file.suffix}"
            elif action == 'number':
                digits = len(str(kwargs.get('start', 1) + len(files) - 1))
                num = kwargs.get('start', 1) + (i-1) * kwargs.get('step', 1)
                new_name = f"{str(num).zfill(digits)}_{file.name}"
            elif action == 'replace':
                new_name = file.name.replace(kwargs['old'], kwargs['new'])
            else:
                new_name = file.name
            print(f"  {i}. {file.name} → {new_name}")


def main():
    parser = argparse.ArgumentParser(description='批量文件重命名工具')
    parser.add_argument('directory', help='目标目录')
    parser.add_argument('-a', '--action', required=True,
                       choices=['prefix', 'suffix', 'number', 'replace', 'regex', 'case', 'date'],
                       help='操作类型')
    parser.add_argument('-p', '--prefix', help='前缀(用于prefix)')
    parser.add_argument('-s', '--suffix', help='后缀(用于suffix)')
    parser.add_argument('--start', type=int, default=1, help='起始序号(用于number)')
    parser.add_argument('--step', type=int, default=1, help='序号步长(用于number)')
    parser.add_argument('--old', help='要替换的文本(用于replace)')
    parser.add_argument('--new', default='', help='替换为(用于replace/regex)')
    parser.add_argument('--pattern-regex', help='正则表达式(用于regex)')
    parser.add_argument('--case', choices=['upper', 'lower', 'title'], help='大小写(用于case)')
    parser.add_argument('--date-format', default='%Y%m%d', help='日期格式(用于date)')
    parser.add_argument('--filter', default='*', help='文件匹配模式')
    parser.add_argument('--preview', action='store_true', help='仅预览，不执行')

    args = parser.parse_args()

    try:
        renamer = BatchRenamer(args.directory)

        if args.preview:
            renamer.preview(args.action, prefix=args.prefix, suffix=args_suffix,
                          start=args.start, step=args.step, old=args.old, new=args.new,
                          pattern=args.filter)
            return

        if args.action == 'prefix':
            if not args.prefix:
                print("❌ prefix 操作需要指定 --prefix")
                return
            renamer.add_prefix(args.prefix, args.filter)

        elif args.action == 'suffix':
            if not args.suffix:
                print("❌ suffix 操作需要指定 --suffix")
                return
            renamer.add_suffix(args.suffix, args.filter)

        elif args.action == 'number':
            renamer.add_number(args.start, args.step, args.filter)

        elif args.action == 'replace':
            if not args.old:
                print("❌ replace 操作需要指定 --old")
                return
            renamer.replace_text(args.old, args.new, args.filter)

        elif args.action == 'regex':
            if not args.pattern_regex:
                print("❌ regex 操作需要指定 --pattern-regex")
                return
            renamer.regex_replace(args.pattern_regex, args.new, args.filter)

        elif args.action == 'case':
            if not args.case:
                print("❌ case 操作需要指定 --case")
                return
            renamer.change_case(args.case, args.filter)

        elif args.action == 'date':
            renamer.add_date(args.date_format, args.filter)

    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    main()
