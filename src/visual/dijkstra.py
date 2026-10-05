def find_path(
    maze: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    if start == goal:
        return [start]

    w = len(maze[0])
    h = len(maze)
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

        cell = maze[y][x]
        if cell == 15:
            continue

        for bit, dx, dy in ((1, 0, -1), (4, 0, 1), (2, 1, 0), (8, -1, 0)):
            if cell & bit:
                continue
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue
            if maze[ny][nx] == 15:
                continue
            nxt = (nx, ny)
            if nxt in prev:
                continue
            prev[nxt] = (x, y)
            queue.append(nxt)

    return []
