import json
import copy

def findLMRow(cur_matrix: list[list], start_row: int) -> tuple[int, int]:
    bestRow = start_row
    bestCol = float("inf")
    for rowIndex in range(start_row, len(cur_matrix)):
        row = cur_matrix[rowIndex]
        leftMostNonZeroIndex = -1
        for colIndex in range(len(row)):
            value = row[colIndex]
            if value != 0:
                leftMostNonZeroIndex = colIndex
                break

        if leftMostNonZeroIndex < bestCol:
            bestRow = rowIndex
            bestCol = leftMostNonZeroIndex

    return (bestRow, bestCol)

def interchangeRows(cur_matrix: list[list], row1: int, row2: int) -> None:
    temp = cur_matrix[row1].copy()
    cur_matrix[row1] = cur_matrix[row2]
    cur_matrix[row2] = temp

def scaleToMake1(cur_matrix: list[list], rowIndex: int, columnIndex: int) -> None:
    value = cur_matrix[rowIndex][columnIndex]
    factor = 1 / value

    # Multiply the whole row by some factor to make the current leading entry to be 1.
    for columnIndex in range(len(cur_matrix[rowIndex])):
        # Round to 2 to avoid floating point stuff.
        entry = cur_matrix[rowIndex][columnIndex]
        new_value = round(entry * factor, 2)
        if new_value % 1 == 0:
            new_value = int(new_value)
        cur_matrix[rowIndex][columnIndex] = new_value
        

def rowAdd(cur_matrix: list[list], rowToAddTo: int, rowToAdd: int, factor: float) -> None:
    
    for columnIndex in range(len(cur_matrix[rowToAddTo])):
        entry = cur_matrix[rowToAddTo][columnIndex]
        added_value = factor * cur_matrix[rowToAdd][columnIndex]
        

        new_value = round(entry + added_value, 2)
        if new_value % 1 == 0:
            new_value = int(new_value)

        cur_matrix[rowToAddTo][columnIndex] = new_value

def matrix_reduce(matrix: list[list]) -> list[list]:
    # Need a deep copy because of nested lists
    cur_matrix = copy.deepcopy(matrix)
    for recursedRow in range(len(cur_matrix)):
        # Need to find row with leftmost non-zero entry
        LMRowIndex, col = findLMRow(cur_matrix, recursedRow)
        interchangeRows(cur_matrix, recursedRow, LMRowIndex)
        scaleToMake1(cur_matrix, LMRowIndex, col)
        for rowIndex in range(len(cur_matrix)):
            if(rowIndex == recursedRow):
                continue

            factor = -cur_matrix[rowIndex][col]
            rowAdd(cur_matrix, rowIndex, LMRowIndex, factor)

    return cur_matrix
                


def main():
    inp = input("Enter the matrix (for example: [[1, 2], [3, 4]]): ")
    matrix = []
    # Convert the string representation of matrix to object via json.
    # If error, catched and main is recalled
    try:
        matrix = json.loads(inp)
    except:
        print("Bad matrix input, try again")
        main()
    
    rref_matrix = matrix_reduce(matrix)
    for row in rref_matrix:
        print(f"{row}")

if __name__ == "__main__":
    main()