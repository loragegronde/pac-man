from PIL import Image

image = Image.open("assets/pacman.png")

# Définit la taille maximale (largeur_max, hauteur_max) tout en gardant les proportions
image.thumbnail((32, 32), Image.Resampling.LANCZOS)

image.save("assets/pacman.png")
