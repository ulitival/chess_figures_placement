from math import floor, factorial, exp


def solve_knight(N: int) -> int:
    return 1 if N == 1 else int(((N**(2*N))/factorial(N))*exp(-9/2))


def solve_bishop(N: int) -> int:
    if N == 1:
        return 1

    def solve_bishop_left(ind: int) -> float:
        sum_left = 0
        for m in range(1, N - ind + 1):
            sum_left += ((-1) ** m * m ** floor(N / 2) * (m + 1) ** floor((N + 1) / 2)) / (
                factorial(N - ind - m) * factorial(m)
            )
        return sum_left

    def solve_bishop_right(ind: int) -> float:
        sum_right = 0
        for m in range(1, ind + 1):
            sum_right += ((-1) ** m * m ** floor((N + 1) / 2) * (m + 1) ** floor(N / 2)) / (
                factorial(ind - m) * factorial(m)
            )
        return sum_right

    return int(((-1) ** N) * sum(solve_bishop_left(ind) * solve_bishop_right(ind) for ind in range(1, N)))

def solve_rook(N: int) -> int:
    return factorial(N)

N = 9
print("Bishop:")
for n in range(1, N):
    print(solve_bishop(n))

print("Knight:")
for n in range(1, N):
    print(solve_knight(n))

print("Rook:")
for n in range(1, N):
    print(solve_rook(n))
