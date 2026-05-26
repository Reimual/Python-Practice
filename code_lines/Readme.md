# 说明

统计Python文件实际代码行数的工具

## 更新日志

-2026.5.26：

上传Github

## 下一步改进

-2026.5.26：

1. 多文件代码行数分别计算与累计计算
2. \*.py文件类型识别

## 学习到的新知识

-2026.5.26：

### argprase的基本使用

```python
import argprase

def main():
    parser = argparse.ArgumentParser(
        prog="*.py",    # 程序名
        description="Count lines of code"    # 描述
    )

    # 定义命令参数选项
    parser.add_argument('src', help="source code file")

    # 如果命令参数值均有效，则返回一个类型为Namespace的结果
    arg = parser.parse_args()

    # 打印命令行参数值（可以直接通过访问定义的命令参数名来取值）
    print(arg.src)


if __name__ == '__main__':
    main()
```