import itertools
import multiprocessing
import sys
import time

from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=.,'
MAX_LENGTH = 5
POOL_SIZE = 3

filename = sys.argv[1]

# load guesses
with open("guess.txt", "r") as f:
    guesses = [line.strip() for line in f]


def passwords():
    for guess in guesses:
        for length in range(1, MAX_LENGTH):
            for pw in itertools.product(CHARS, repeat=length):
                yield '{}{}'.format(guess, ''.join(pw))


def check_password(p: str):
    try:
        print(f"Trying {p}...")
        PyKeePass(filename, password=p)
        print(f"FOUND: Password is '{p}'")
        return True
    except CredentialsError:
        return False


# Start a timer
start = time.perf_counter()

with multiprocessing.Pool(POOL_SIZE) as pool:
    # Use map() to apply the calculate_square function to each element in the input list
    result_iterator = pool.imap(check_password, passwords())

    # Iterate over the results and print them
    i = 0
    for result in result_iterator:
        i += 1
        if result:
            # Stop the worker processes and exit the loop
            pool.terminate()
            break

    print(f"Tried {i} passwords")

# End the timer and print the elapsed time
end = time.perf_counter()
print(f"Elapsed time: {end - start:0.6f} seconds")
