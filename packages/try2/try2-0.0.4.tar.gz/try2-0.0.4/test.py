from src.try2 import try2

def reciprocal(n):
    return 1 / n

ls = [1, 2, 0, 3, 0, 4]

for number in ls:
    x = try2(reciprocal, number, "bad")
    print(number, "=>", x)

# 1 => 1.0
# 2 => 0.5
# 0 => bad
# 3 => 0.3333333333333333
# 0 => bad
# 4 => 0.25
