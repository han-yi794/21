import sys
import math

def prime_generator():
    primes = []
    n = 2
    while True:
        is_prime = True
        limit = int(math.isqrt(n))
        for p in primes:
            if p > limit:
                break
            if n % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(n)
            yield n
        if n == 2:
            n = 3
        else:
            n += 2

def print_primes(mode, value):
    gen = prime_generator()
    if mode == 'count':
        try:
            count = int(value)
            if count <= 0:
                raise ValueError
            print(f"前 {count} 个质数：")
            for i in range(1, count + 1):
                p = next(gen)
                print(f"第{i}个质数是 {p}")
        except ValueError:
            print("错误：数量必须是正整数。")
    elif mode == 'limit':
        try:
            limit = int(value)
            if limit < 2:
                print("没有不小于2的质数。")
                return
            print(f"不超过 {limit} 的质数：")
            i = 1
            for p in gen:
                if p > limit:
                    break
                print(f"第{i}个质数是 {p}")
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
            print_primes('count', value)
        elif mode in ('-l', '--limit'):
            print_primes('limit', value)
        else:
            print("用法：")
            print("  python primes.py --count <数量>")
            print("  python primes.py --limit <上限>")
            print("示例：")
            print("  python primes.py --count 10")
            print("  python primes.py --limit 100")
    else:
        # 无限输出模式：英文，避免乱码
        print("Generating primes infinitely (press Ctrl+C to stop):")
        try:
            for i, p in enumerate(prime_generator(), start=1):
                print(f"Prime #{i} is {p}", flush=True)
        except KeyboardInterrupt:
            print("\nStopped by user.")

if __name__ == "__main__":
    main()
