"""
Name: YOUR NAME
SID: YOUR SID
File: boggle_solver.py
"""

# No external libraries; keep it plain Python.

class Boggle:
    def __init__(self, grid=None, dictionary=None):
        self.grid = []
        self.rows = 0
        self.cols = 0
        self.dictionary = set()
        self.prefixes = set()
        self._solution = []
        if grid is not None:
            self.setGrid(grid)
        if dictionary is not None:
            self.setDictionary(dictionary)

    # ----- required API -----
    def setGrid(self, grid):
        # Normalize to UPPERCASE; tiles can be multi-letter like "Qu", "St", "Ie"
        self.grid = [[str(cell).upper() for cell in row] for row in grid]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows else 0

    def setDictionary(self, words):
        up = [str(w).upper() for w in words if w]
        self.dictionary = set(up)
        # Build prefix set for pruning
        prefixes = set()
        for w in up:
            for i in range(1, len(w) + 1):
                prefixes.add(w[:i])
        self.prefixes = prefixes

    def getSolution(self):
        # Compute on demand so tests that call getSolution() directly work
        return self.solution()

    # ----- solver -----
    def solution(self, min_len=3):
        if not self.grid or not self.dictionary:
            self._solution = []
            return self._solution

        found = set()
        visited = [[False] * self.cols for _ in range(self.rows)]

        def neighbors(r, c):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        yield nr, nc

        def dfs(r, c, prefix):
            word = prefix + self.grid[r][c]  # multi-letter tile support
            if word not in self.prefixes:
                return  # prune if no dictionary word starts with this

            if len(word) >= min_len and word in self.dictionary:
                found.add(word)

            visited[r][c] = True
            for nr, nc in neighbors(r, c):
                if not visited[nr][nc]:
                    dfs(nr, nc, word)
            visited[r][c] = False

        for i in range(self.rows):
            for j in range(self.cols):
                dfs(i, j, "")

        self._solution = sorted(found)
        return self._solution


# Demo main (ignored by autograder; safe to leave)
def main():
    grid = [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
    ]
    dictionary = ["ABC", "ABE", "ABDHIE", "FED", "AGE"]
    game = Boggle(grid, dictionary)
    print(game.getSolution())


if __name__ == "__main__":
    main()
