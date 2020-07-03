class SudokuFunctions:

    # Solving function #
    @staticmethod
    def solve(tab):
        find = SudokuFunctions.find_empty(tab)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1,10):
            if SudokuFunctions.isvalide(tab,i,(row, col)):
                tab[row][col] = i

                if SudokuFunctions.solve(tab):
                    return True

                tab[row][col] = 0

        return False

    # Checking if the current solution is valid #
    @staticmethod
    def isvalide(tab, nr, poz):

        for i in range(len(tab[0])):
            if tab[poz[0]][i] == nr and poz[1] != i:
                return False

        for i in range(len(tab)):
            if tab[i][poz[1]] == nr and poz[0] !=i:
                return False

        yBox = poz[0] // 3
        xBox = poz[1] // 3

        for i in range(yBox*3,yBox*3 + 3):
            for j in range(xBox * 3, xBox * 3 + 3):
                if tab[i][j] == nr and (i,j) != poz:
                    return False
        return True

    # Graphical delimitation of tab #
    @staticmethod
    def delimitate(tab):
        for i in range(len(tab)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - - ")

            for j in range(len(tab[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(tab[i][j])
                else:
                    print(str(tab[i][j]) + " ", end="")


    # Finding the first empty element in our way #
    @staticmethod
    def find_empty(tab):
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i][j] == 0:
                    return (i, j)
        return None

