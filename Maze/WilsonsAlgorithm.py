from random import randint, shuffle

default_width = 10
default_height = 5
N, S, E, W = 1, 2, 4, 8 #Flags for encoding connection
DX =       {E:1, W:-1, N:0, S:0}
DY =       {E:0, W:0, N:-1, S:1}
OPPOSITE = {E:W, W:E, N:S, S:N}

def print_maze(grid):
	# print grid
	# for row in grid:
	# 	line = ""
	# 	for cell in row:
	# 		if cell >= 8:
	# 			line += "+ "
	# 		else:
	# 			line += "+-"
	# 	print line + "+"
	# 	line = ""
	# 	for cell in row:
	# 		if cell%8%4 >= 2:
	# 			line += "| "
	# 		else:
	# 			line += "  "
	# 	print line + "|"
	# print "+-"*len(row) + "+"

	print grid
	for i in range(len(grid[0])):
		row = ""
		for column in grid:
			if column[i]%8%4%2 == 1:
				row +=  "+ "
			else:
				row += "+-"
		print row + "+"
		row = ""
		for column in grid:
			if column[i] >= 8:
				row += "  "
			else:
				row += "| "
		print row + "|"
	print '+-'*len(grid) + '+'



def generate_maze(width = default_width, height = default_height):
	''' Generates an array that contains
	'''
	grid = [[0 for i in range(height)] for j in range(width)]
	#print grid
	grid[randint(0,width-1)][randint(0,height-1)] = 'Initial'
	remaining = width*height -1 # of unused cells
	#print "Starting Walk"
	while remaining > 0:
		#print "Remaining " + str(remaining)
		path = walk(grid)
		for i in path:
			x,y,direction = i[0], i[1], i[2]
			nx, ny = x + DX[direction], y + DY[direction]
			grid[x][y] += direction
			if grid[nx][ny] == "Initial":
				grid[nx][ny] = OPPOSITE[direction]
			else:
				grid[nx][ny] += OPPOSITE[direction]
			remaining -= 1
	return grid


def walk(grid):
	''' Chooses a random point, and executes a
		random walk untill it connects to the
		existing maze
	'''
	#Find a point to start from
	startPoint = False
	while not startPoint:
		cx, cy = randint(0, len(grid)-1), randint(0, len(grid[0])-1)
		if grid[cx][cy] == 0:
			startPoint = True

	#Initialize dictionary to inicate how the cell was exited.
	visits = {(cy, cx):0}
	start_x, start_y = cx, cy #Where the random walk started
	walking = True #whether the path has connected
	while walking:
		directions = [N,S,E,W]
		shuffle(directions)
		for i in directions:
			#Tests directions untill it finds a usable one
			nx, ny = cx + DX[i], cy + DY[i] #neighboring cell coordinates
			if nx >= 0 and ny >=0 and nx<len(grid) and ny <len(grid[nx]):
				visits[(cx, cy)] = i
				if grid[nx][ny] != 0:
					#Stop walking, exit loop
					walking = False
					break
				else:
					#Continue walking
					cx, cy = nx, ny
					break
					

	#Create the path from known directions
	path = []
	x,y = start_x, start_y
	while (x,y) != (nx, ny):
		direction = visits[(x,y)]
		path.append((x,y,direction))
		x, y = x + DX[direction], y + DY[direction]
	return path

if __name__ == '__main__':
	maze = generate_maze()
	print_maze(maze)




