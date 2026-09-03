# Pac-Man

## Config keys (`config.json`)

Comments are supported: lines starting with `#`, `//` blocks are ignored.

- highscore_filename
- width
- height
- lives
- pacgum
- points_per_pacgum
- points_per_super_pacgum
- points_per_ghost
- seed
- level_max_time


On missing or invalid values, the game clamps to safe defaults and logs a warning.
Unknown keys are silently ignored.

---

## Graphics — MLX equivalents using pygame

| MLX | Pygame equivalent |
|-----|-------------------|
| `mlx_init()` | `pygame.init()` |
| `mlx_release()` / `mlx_destroy_display()` | `pygame.quit()` |
| `mlx_new_window(w, h, title)` | `pygame.display.set_mode((w, h))` + `pygame.display.set_caption(title)` |
| `mlx_clear_window()` | `surface.fill((0, 0, 0))` |
| `mlx_destroy_window()` | `pygame.display.quit()` |
| `mlx_pixel_put(x, y, color)` | `surface.set_at((x, y), color_rgb)` |
| `mlx_string_put(x, y, color, text)` | `font.render(text, True, color_rgb)` + `screen.blit(surf, (x, y))` |
| `mlx_new_image(w, h)` | `pygame.Surface((w, h))` |
| `mlx_get_data_addr()` | `surface.get_view("3")` / `pygame.surfarray` |
| `mlx_put_image_to_window(x, y)` | `screen.blit(surface, (x, y))` |
| `mlx_png_file_to_image(filename)` | `pygame.image.load(filename).convert_alpha()` |
| `mlx_xpm_file_to_image(filename)` | `pygame.image.load(filename)` (convert XPM to PNG first) |
| `mlx_destroy_image()` | `del surface` |
| `img.pixel_put(x, y, color)` | `surface.set_at((x, y), color_rgb)` |
| `img.pixel_get(x, y)` | `surface.get_at((x, y))` |
| `img.clear(color)` | `surface.fill(color_rgb)` |
| `img.draw_rect(x, y, w, h, color)` | `pygame.draw.rect(surface, color_rgb, (x, y, w, h))` |
| `img.draw_rect_outline(x, y, w, h, color, thickness)` | `pygame.draw.rect(surface, color_rgb, (x, y, w, h), thickness)` |
| `img.draw_line(x0, y0, x1, y1, color)` | `pygame.draw.line(surface, color_rgb, (x0, y0), (x1, y1))` |
| `img.draw_line_thick(x0, y0, x1, y1, color, thickness)` | `pygame.draw.line(surface, color_rgb, (x0, y0), (x1, y1), thickness)` |
| `img.draw_circle(cx, cy, radius, color)` | `pygame.draw.circle(surface, color_rgb, (cx, cy), radius)` |
| `img.draw_circle_outline(cx, cy, radius, color, thickness)` | `pygame.draw.circle(surface, color_rgb, (cx, cy), radius, thickness)` |
| `img.draw_triangle(x0, y0, x1, y1, x2, y2, color)` | `pygame.draw.polygon(surface, color_rgb, [(x0,y0),(x1,y1),(x2,y2)])` |
| `img.draw_triangle_outline(x0, y0, x1, y1, x2, y2, color)` | `pygame.draw.polygon(surface, color_rgb, [(x0,y0),(x1,y1),(x2,y2)], 1)` |
| `img.draw_gradient_h(x, y, w, h, c_left, c_right)` | manual loop: `surface.set_at((x+i, y+j), lerp(c_left, c_right, i/w))` |
| `img.draw_gradient_v(x, y, w, h, c_top, c_bottom)` | manual loop: `surface.set_at((x+i, y+j), lerp(c_top, c_bottom, j/h))` |
| `img.draw_polygon(points, color)` | `pygame.draw.polygon(surface, color_rgb, points, 1)` |
| `img.flood_fill(x, y, color)` | manual BFS/stack loop on `surface.get_at` / `set_at` |
| `mlx_loop()` | `while running: pygame.event.get()` |
| `mlx_loop_end()` | `running = False` |
| `mlx_loop_hook(callback)` | call `callback()` at the end of each loop iteration |
| `mlx_key_hook(callback)` | handle `pygame.KEYDOWN` events |
| `mlx_mouse_hook(callback)` | handle `pygame.MOUSEBUTTONDOWN` events |
| `mlx_expose_hook(callback)` | handle `pygame.VIDEOEXPOSE` (window needs redraw) |
| `mlx_mouse_hide()` | `pygame.mouse.set_visible(False)` |
| `mlx_mouse_show()` | `pygame.mouse.set_visible(True)` |
| `mlx_mouse_move(x, y)` | `pygame.mouse.set_pos((x, y))` |
| `mlx_mouse_get_pos()` | `pygame.mouse.get_pos()` |
| `mlx_get_screen_size()` | `pygame.display.Info().current_w / current_h` |
| `mlx_do_sync()` | `pygame.display.flip()` |
| `mlx_do_key_autorepeatoff()` | `pygame.key.set_repeat(0)` |
| `mlx_do_key_autorepeaton()` | `pygame.key.set_repeat(delay, interval)` |

---

## Authors

- acampion — parsing
- eel-kerc