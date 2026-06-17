"""
Excel 自动化处理工具
功能：批量合并、数据提取、去重清洗、生成报表
"""

import os
import sys
import pandas as pd
from pathlib import Path
import argparse
from datetime import datetime


class ExcelTool:
    """Excel 自动化处理工具"""

    def __init__(self):
        self.data = None

    def merge_files(self, input_dir, output_file="merged.xlsx"):
        """批量合并目录下所有 Excel 文件"""
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"❌ 目录不存在: {input_dir}")
            return None

        excel_files = list(input_path.glob("*.xlsx")) + list(input_path.glob("*.xls"))
        if not excel_files:
            print(f"❌ 目录中没有找到 Excel 文件: {input_dir}")
            return None

        print(f"📁 找到 {len(excel_files)} 个 Excel 文件")

        all_data = []
        for file in excel_files:
            try:
                df = pd.read_excel(file)
                df['_来源文件'] = file.name
                all_data.append(df)
                print(f"  ✅ 已读取: {file.name} ({len(df)} 行)")
            except Exception as e:
                print(f"  ❌ 读取失败: {file.name} - {e}")

        if not all_data:
            print("❌ 没有成功读取任何文件")
            return None

        merged = pd.concat(all_data, ignore_index=True)
        merged.to_excel(output_file, index=False)
        print(f"\n✅ 合并完成: {output_file}")
        print(f"   总行数: {len(merged)}")
        print(f"   总列数: {len(merged.columns)}")
        self.data = merged
        return merged

    def extract_columns(self, input_file, columns, output_file="extracted.xlsx"):
        """提取指定列数据"""
        try:
            df = pd.read_excel(input_file)
            available = [c for c in columns if c in df.columns]
            missing = [c for c in columns if c not in df.columns]

            if missing:
                print(f"⚠️ 以下列不存在: {missing}")
                print(f"   可用列: {list(df.columns)}")

            if not available:
                print("❌ 没有可提取的列")
                return None

            extracted = df[available]
            extracted.to_excel(output_file, index=False)
            print(f"✅ 提取完成: {output_file}")
            print(f"   提取列: {available}")
            print(f"   行数: {len(extracted)}")
            self.data = extracted
            return extracted

        except Exception as e:
            print(f"❌ 提取失败: {e}")
            return None

    def remove_duplicates(self, input_file, columns=None, output_file="deduplicated.xlsx"):
        """数据去重"""
        try:
            df = pd.read_excel(input_file)
            original_count = len(df)

            if columns:
                available = [c for c in columns if c in df.columns]
                if not available:
                    print(f"❌ 指定的列都不存在: {columns}")
                    return None
                df = df.drop_duplicates(subset=available)
            else:
                df = df.drop_duplicates()

            removed = original_count - len(df)
            df.to_excel(output_file, index=False)
            print(f"✅ 去重完成: {output_file}")
            print(f"   原始行数: {original_count}")
            print(f"   去重后: {len(df)}")
            print(f"   移除重复: {removed}")
            self.data = df
            return df

        except Exception as e:
            print(f"❌ 去重失败: {e}")
            return None

    def clean_data(self, input_file, output_file="cleaned.xlsx"):
        """数据清洗：去除空行、空格、标准化格式"""
        try:
            df = pd.read_excel(input_file)
            original_count = len(df)

            # 去除完全空的行
            df = df.dropna(how='all')

            # 去除字符串列的首尾空格
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace('nan', pd.NA)

            # 去除重复行
            df = df.drop_duplicates()

            removed = original_count - len(df)
            df.to_excel(output_file, index=False)
            print(f"✅ 清洗完成: {output_file}")
            print(f"   原始行数: {original_count}")
            print(f"   清洗后: {len(df)}")
            print(f"   清理行数: {removed}")
            self.data = df
            return df

        except Exception as e:
            print(f"❌ 清洗失败: {e}")
            return None

    def generate_report(self, input_file, output_file="report.xlsx"):
        """生成汇总报表"""
        try:
            df = pd.read_excel(input_file)

            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                # 原始数据
                df.to_excel(writer, sheet_name='原始数据', index=False)

                # 统计摘要
                summary_data = []
                for col in df.columns:
                    info = {
                        '列名': col,
                        '数据类型': str(df[col].dtype),
                        '非空值数': df[col].count(),
                        '空值数': df[col].isna().sum(),
                        '唯一值数': df[col].nunique()
                    }
                    if df[col].dtype in ['int64', 'float64']:
                        info['最小值'] = df[col].min()
                        info['最大值'] = df[col].max()
                        info['平均值'] = round(df[col].mean(), 2)
                        info['总和'] = df[col].sum()
                    summary_data.append(info)

                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='列统计', index=False)

                # 数值列统计
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) > 0:
                    desc = df[numeric_cols].describe()
                    desc.to_excel(writer, sheet_name='数值统计')

            print(f"✅ 报表生成完成: {output_file}")
            print(f"   包含工作表: 原始数据, 列统计, 数值统计")
            return output_file

        except Exception as e:
            print(f"❌ 报表生成失败: {e}")
            return None


def main():
    parser = argparse.ArgumentParser(description='Excel 自动化处理工具')
    parser.add_argument('action', choices=['merge', 'extract', 'dedup', 'clean', 'report'],
                       help='操作类型: merge=合并, extract=提取, dedup=去重, clean=清洗, report=报表')
    parser.add_argument('-i', '--input', required=True, help='输入文件或目录')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-c', '--columns', nargs='+', help='要提取的列名(用于extract)')
    parser.add_argument('-d', '--dedup-cols', nargs='+', help='去重依据的列名(用于dedup)')

    args = parser.parse_args()
    tool = ExcelTool()

    if args.action == 'merge':
        output = args.output or 'merged.xlsx'
        tool.merge_files(args.input, output)

    elif args.action == 'extract':
        if not args.columns:
            print("❌ extract 操作需要指定 -c/--columns 参数")
            sys.exit(1)
        output = args.output or 'extracted.xlsx'
        tool.extract_columns(args.input, args.columns, output)

    elif args.action == 'dedup':
        output = args.output or 'deduplicated.xlsx'
        tool.remove_duplicates(args.input, args.dedup_cols, output)

    elif args.action == 'clean':
        output = args.output or 'cleaned.xlsx'
        tool.clean_data(args.input, output)

    elif args.action == 'report':
        output = args.output or 'report.xlsx'
        tool.generate_report(args.input, output)


if __name__ == '__main__':
    main()
