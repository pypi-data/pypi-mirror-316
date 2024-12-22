from typing import List

class TranspositionMatrix:
    def __init__(self, key):
        self.key = key
    
    @staticmethod
    def __validate_key(key: str | int) -> List[int]:
        try:
            key = int(key)
        except:
            raise ValueError("Key charcters should be numbers only")
        key_digits = []
        max_digit = float("-inf")
        min_digit = float("inf")
        while key > 0:
            digit = key % 10
            key_digits.append(digit)
            if digit > max_digit:
                max_digit = digit
            if min_digit > digit:
                min_digit = digit
            key //= 10
        if len(key_digits) != max_digit - min_digit + 1:
            raise ValueError("Key should be a continuous digits")
        return key_digits[::-1]
    
    @staticmethod
    def __plantext_to_matrix(plantext: str, columns: int) -> List[List]:
        matrix = []
        row = []
        index = 0
        while index < len(plantext):
            row.append(plantext[index])
            if len(row) == columns:
                matrix.append(row)
                row = []
            index += 1
        if len(row):
            while len(row) < columns:
                row.append("")
            matrix.append(row)
        return matrix

    @staticmethod
    def encrypt(plantext: str, key: str | int) -> str:
        key_digits = TranspositionMatrix.__validate_key(key) 
        plantext_matrix = TranspositionMatrix.__plantext_to_matrix(plantext, len(key_digits))
        cipher = []
        columns = list(zip(*plantext_matrix))
        for column in key_digits:
            cipher.extend(columns[column - 1])
        return "".join(cipher)

    @staticmethod
    def decrypt(ciphertext: str, key: str | int) -> str:
        key_digits = TranspositionMatrix.__validate_key(key)
        num_columns = len(key_digits)
        num_rows = len(ciphertext) // num_columns
        remaining_chars = len(ciphertext) % num_columns

        column_lengths = [num_rows + 1 if i < remaining_chars else num_rows for i in range(num_columns)]

        columns = []
        index = 0
        for col_length in column_lengths:
            columns.append(ciphertext[index:index + col_length])
            index += col_length

        reordered_columns = [""] * num_columns
        for i, key_digit in enumerate(key_digits):
            reordered_columns[key_digit - 1] = columns[i]

        plaintext_matrix = []
        for row_index in range(num_rows + (1 if remaining_chars > 0 else 0)):
            row = []
            for col in reordered_columns:
                if row_index < len(col):
                    row.append(col[row_index])
            plaintext_matrix.append(row)

        return "".join([char for row in plaintext_matrix for char in row if char])
