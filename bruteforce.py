import itertools
import multiprocessing
import plac
import sys
import time

from pykeepass import PyKeePass
from pykeepass.exceptions import CredentialsError


class PyKeePassBrute:
    CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=.,'
    MAX_LENGTH = 5
    POOL_SIZE = 3

    def __init__(self):
        self.filename = sys.argv[1]

        # load guesses
        with open("guesses.txt", "r") as f:
            self.guesses = [line.strip() for line in f]

    def main(self):
        # Start a timer
        start = time.perf_counter()

        with multiprocessing.Pool(self.POOL_SIZE) as pool:
            # Use map() to apply the calculate_square function to each element in the input list
            result_iterator = pool.imap(self.check_password, self.passwords())

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

    def check_password(self, p: str):
        try:
            print(f"Trying {p}...")
            PyKeePass(self.filename, password=p)
            print(f"FOUND: Password is '{p}'")
            return True
        except CredentialsError:
            return False

    def passwords(self):
        for guess in self.guesses:
            for length in range(1, self.MAX_LENGTH):
                for pw in itertools.product(self.CHARS, repeat=length):
                    yield '{}{}'.format(guess, ''.join(pw))


if __name__ == "__main__":
    pkpb = PyKeePassBrute()
    plac.call(pkpb.main)
