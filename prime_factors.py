import time
import sqlite3
import os


DB_FILE = "prime_factors.db"


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


def write_to_txt(input_integer: int, prime_factors: list[int], elapsed_time: str):
    """
    Saves output into a text file. Asked number, its prime factors and elapsed time.
    """
    factors_str = ", ".join(map(str, prime_factors))

    output = output = (
        "Prime Factors |\n"
        "------------------------------\n"
        f"Number        : {input_integer}\n"
        f"Prime Factors : {factors_str}\n"
        f"Time Taken    : {elapsed_time:.4f} seconds\n"
    )

    with open("prime_factors_output.txt", "w", encoding="utf-8") as f:
        f.write(output)


def initialize_database(database_path: str = DB_FILE) -> sqlite3.Connection:
    """
    Creates a sqlite dabatase and table if not exists. Returns a connection.
    """
    database_exists = os.path.exists(database_path)
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Create table if missing
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS prime_factors (
            input_number INTEGER PRIMARY KEY,
            factors TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()

    if not database_exists:
        print(f"Database created at {database_path}\n")
    else:
        print(f"Database already exists at {database_path}\n")

    return conn


def get_factors_from_db(conn: sqlite3.Connection, input_number: int):
    """
    Return a list of prime factors (list[int]) if exists in DB, otherwise None.
    Prime factors are stored as a string and need to be changed back to list[int]
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT factors FROM prime_factors WHERE input_number = ?", (input_number,)
    )
    row = cursor.fetchone()
    if row:
        factors = [int(x) for x in row[0].split(",")]
        print(f"Number {input_number} found in the database with its prime factors.")
        return factors
    return None


def save_factors_to_db(
    conn: sqlite3.Connection, input_number: int, prime_factors: list[int]
):
    """
    Insert a new number and its factors into DB.
    Prime factors are stored as a string as sqlite does not support list.
    """
    cursor = conn.cursor()
    factors_str = ",".join(map(str, prime_factors))
    cursor.execute(
        "INSERT OR REPLACE INTO prime_factors (input_number, factors) VALUES (?, ?)",
        (input_number, factors_str),
    )
    conn.commit()
    print(f"\nNumber {input_number} with its prime factors saved into the database.")


def main():
    # Initialize database if it does not exist
    dbconn = initialize_database()

    # Get user input and validate it
    while True:
        user_input = input("Give me the number: ")
        input_integer = validate_user_input(user_input)
        if input_integer:
            break

    # Try and fetch input from database
    start_time = time.perf_counter()
    prime_factors_db = get_factors_from_db(dbconn, input_integer)
    if not prime_factors_db:
        # Calculate prime factors and return unique prime factors
        prime_factors = get_unique_prime_factors(input_integer)
    else:
        prime_factors = prime_factors_db
    print_prime_factors(prime_factors)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"It took {elapsed_time:.4f} seconds to find those")

    # Write a fancy txt file of the results
    write_to_txt(input_integer, prime_factors, elapsed_time)

    # If asked number was not in database, save it in to there
    if not prime_factors_db:
        save_factors_to_db(dbconn, input_integer, prime_factors)

    # Finally close up the connection to the database
    dbconn.close()


if __name__ == "__main__":
    main()
