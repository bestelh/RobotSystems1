import atexit
import time
from picarx_improved import Picarx
import ast

def main():
    
    # # Ask the user for a matrix
    # matrix_str = input("Enter a matrix (e.g., [[1, 2], [3, 4]]): ")

    # # Convert the string to a list of lists
    # matrix = ast.literal_eval(matrix_str)

    # # Get the second value of the matrix
    # # This assumes the matrix is at least 2x2
    # test = matrix[0][1]

    # print("The second value of the matrix is:", test)

    input_command= input("Enter Command (action angle speed)": )
    commands_to_array= input_command.split(" ")



if __name__ == "__main__":
    main()