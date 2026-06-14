import sys
import math

# 解除整数转字符串的长度限制（Python 3.11+）
sys.set_int_max_str_digits(0)

# 其余原有代码保持不变...
def is_prime(n: int) -> bool:
    """简单试除法判断正整数是否为素数（n较小）"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True

def lucas_lehmer(p: int) -> bool:
    """
    卢卡斯-莱默测试：判断梅森数 M_p = 2^p - 1 是否为素数。
    适用于奇素数 p，p=2 时直接返回 True。
    """
    if p == 2:
        return True
    if not is_prime(p):
        return False
    m = (1 << p) - 1          # 梅森数 M_p
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0

def perfect_generator():
    """
    完全数生成器（基于梅森素数）。
    依次生成所有偶数完全数，无限迭代。
    """
    p = 2
    while True:
        if lucas_lehmer(p):
            # 完全数 = 2^(p-1) * (2^p - 1)
            perfect = (1 << (p - 1)) * ((1 << p) - 1)
            yield perfect
        # 下一个候选指数 p（必须是素数，但 lucas_lehmer 会自己检查）
        p += 1
        # 跳过偶数（素数除2外都是奇数）
        if p > 2 and p % 2 == 0:
            p += 1

def print_perfects(mode, value):
    """根据模式输出完全数（带序号）"""
    gen = perfect_generator()
    if mode == 'count':
        try:
            n = int(value)
            if n <= 0:
                raise ValueError
            print(f"前 {n} 个完全数：")
            for i in range(1, n + 1):
                perfect = next(gen)
                print(f"第{i}个完全数是 {perfect}")
        except ValueError:
            print("错误：数量必须是正整数。")
    elif mode == 'limit':
        try:
            limit = int(value)
            if limit < 2:
                print("没有小于2的完全数。")
                return
            print(f"不超过 {limit} 的完全数：")
            i = 1
            for perfect in gen:
                if perfect > limit:
                    break
                print(f"第{i}个完全数是 {perfect}")
                i += 1
        except ValueError:
            print("错误：上限必须是整数。")
    else:
        print("未知模式。")

def main():
    if len(sys.argv) == 3:
        mode = sys.argv[1].lower()
        value = sys.argv[2]
        if mode in ('-c', '--count'):
            print_perfects('count', value)
        elif mode in ('-l', '--limit'):
            print_perfects('limit', value)
        else:
            print("用法：")
            print("  python perfect.py --count <数量>     # 输出前N个完全数")
            print("  python perfect.py --limit <上限>     # 输出所有不超过上限的完全数")
            print("示例：")
            print("  python perfect.py --count 5")
            print("  python perfect.py --limit 10000")
    else:
        # 交互模式：无限输出完全数
        print("从第一个完全数开始无限输出（按 Ctrl+C 停止）...")
        try:
            for i, perfect in enumerate(perfect_generator(), start=1):
                print(f"第{i}个完全数是 {perfect}，长度为{len(str(perfect))}", flush=True)
        except KeyboardInterrupt:
            print("\n程序已停止。")

if __name__ == "__main__":
    main()
