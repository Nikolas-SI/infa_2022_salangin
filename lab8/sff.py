line = 'Planet 10 red 1000 1 2 3 4'
type = line.split()[0]
R = int(line.split()[1])
color = line.split()[2]
m, x, y, Vx, Vy = list(map(int, line.split()[3:8]))
print(m)
