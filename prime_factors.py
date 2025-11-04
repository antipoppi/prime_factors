import time


def validate_user_input(input: str) -> int:
    try:
        input_number = int(input)
        if input_number < 1:
            print("Number should not be zero or less.")
        elif input_number == 1:
            print(
                "A prime number is a natural number greater than 1. Please give a greater number."
            )
        else:
            return input_number
    except (ValueError, TypeError):
        print("Please only give whole numbers. (e.g. 26541)")


def is_prime(n: int) -> bool:
    """
    Checks if a number is a prime number and returns True/False.
    """
    if n > 1:
        for i in range(2, n):
            if (n % i) == 0:
                return False
        return True
    else:
        return False


def get_unique_prime_factors(n: int) -> list[int]:
    """
    Function goes through int input and appends prime factors into a list.
    Finally returns unique list of factors.
    """
    factors = []
    i = 2
    while i <= n:
        if n % i == 0 and is_prime(i):
            # append found first factor into factors, divide and continue with quotient
            factors.append(i)
            n = n / i
        else:
            i += 1
    return list(dict.fromkeys(factors))  # return only unique factors


def print_prime_factors(prime_factors: list[int]):
    for n in prime_factors:
        print(f"Prime factor found: {n}")


def main():
    while True:
        user_input = input("Give me the number: ")
        input_integer = validate_user_input(user_input)
        if input_integer:
            break
    start_time = time.perf_counter()
    prime_factors = get_unique_prime_factors(input_integer)
    print_prime_factors(prime_factors)
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"It took {total_time:.4f} seconds to find those")
    # time spent 2,75h
    # TODO: Add timer
    # TODO: Add output file (txt)
    # TODO: Add database


if __name__ == "__main__":
    main()
