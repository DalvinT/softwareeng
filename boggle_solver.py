"""
Name: YOUR NAME
SID: YOUR SID
File: boggle_solver.py
"""

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

    def setGrid(self, grid):
        # Keep multi-letter tiles intact; normalize to UPPERCASE
        self.grid = [[str(cell).upper() for cell in row] for row in (grid or [])]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows else 0

    def setDictionary(self, words):
        words = [str(w).upper() for w in (words or []) if w]
        self.dictionary = set(words)
        # prefix set for pruning
        p = set()
        for w in words:
            for i in range(1, len(w) + 1):
                p.add(w[:i])
        self.prefixes = p

    def getSolution(self):
        # Compute on demand so outside tests can just call this
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
            # Tiles can be multi-letter: "QU", "ST", "IE", etc.
            word = prefix + self.grid[r][c]
            if word not in self.prefixes:
                return
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
