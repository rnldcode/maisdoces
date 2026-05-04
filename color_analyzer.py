from PIL import Image
import numpy as np

# Abre a imagem
img = Image.open('maisdoces-front/src/images/bolodecorado.png').convert('RGB')
pixels = np.array(img)

# Obtém cores únicas e contagens
colors, counts = np.unique(pixels.reshape(-1, 3), axis=0, return_counts=True)

# Ordena por contagem (mais frequentes primeiro)
sorted_indices = np.argsort(counts)[::-1]

print('Cores mais frequentes (Hex):')
for i in range(20):
    idx = sorted_indices[i]
    color = colors[idx]
    count = counts[idx]
    hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
    print(f'{hex_color} - {count} pixels')

print('\nCores azuis encontradas (Hex):')
for i in range(len(colors)):
    color = colors[i]
    if color[2] > color[0] and color[2] > color[1] and color[2] > 100:
        hex_color = '#%02x%02x%02x' % (color[0], color[1], color[2])
        print(f'{hex_color} - {counts[i]} pixels')
