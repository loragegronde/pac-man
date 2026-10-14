def _neighbors(maze: list[list[int]], x: int, y: int) -> list[tuple[int, int]]:
    w = len(maze[0])
    h = len(maze)
    cell = maze[y][x]
    if cell == 15:
        return []
    out: list[tuple[int, int]] = []
    for bit, dx, dy in ((1, 0, -1), (4, 0, 1), (2, 1, 0), (8, -1, 0)):
        if cell & bit:
            continue
        nx, ny = x + dx, y + dy
        if nx < 0 or ny < 0 or nx >= w or ny >= h:
            continue
        if maze[ny][nx] == 15:
            continue
        out.append((nx, ny))
    return out


def find_path(
    maze: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    if start == goal:
        return [start]

    prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    queue: list[tuple[int, int]] = [start]

    while queue:
        x, y = queue.pop(0)
        if (x, y) == goal:
            path: list[tuple[int, int]] = []
            node: tuple[int, int] | None = goal
            while node is not None:
                path.append(node)
                node = prev[node]
            path.reverse()
            return path

        for nxt in _neighbors(maze, x, y):
            if nxt in prev:
                continue
            prev[nxt] = (x, y)
            queue.append(nxt)

    return []


def farthest_cell(
    maze: list[list[int]],
    from_pos: tuple[int, int],
) -> tuple[int, int]:
    prev: dict[tuple[int, int], None] = {from_pos: None}
    queue: list[tuple[int, int]] = [from_pos]
    farthest = from_pos
    while queue:
        x, y = queue.pop(0)
        farthest = (x, y)
        for nxt in _neighbors(maze, x, y):
            if nxt in prev:
                continue
            prev[nxt] = None
            queue.append(nxt)
    return farthest


def next_cell(
    maze: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> tuple[int, int] | None:
    path = find_path(maze, start, goal)
    return path[1] if len(path) >= 2 else None


def dir_to(a: tuple[int, int], b: tuple[int, int]) -> int:
    ax, ay = a
    bx, by = b
    if by < ay:
        return 1
    if bx > ax:
        return 2
    if by > ay:
        return 4
    return 8
