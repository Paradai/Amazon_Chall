from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import random

#Need to "pip install pathfinding" module to use this

#Assess route function with the given matrix layout with the keypoints
#using A* algorithm used in the pathfinding module.

#Algorithm assesses each route between nodes and seeks a valid path
#ideally the shortest route.

#Grid, path length and number of runs is printed out.

def assess_route(matrix, start_loc, end_loc):
  grid = Grid(matrix=matrix)
  start = grid.node(start_loc[0], start_loc[1])
  end = grid.node(end_loc[0], end_loc[1])

  finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
  path, runs = finder.find_path(start, end, grid)

  print('operations:', runs, 'path length:', len(path))
  print("Path route is:" + str(path))
  print(grid.grid_str(path=path, start=start, end=end, empty_chr="0"))

  path_len = len(path)
  return path_len

#User types number of grid points (x by y), start/end locations (x,y).
#Followed by number of obstacles.

#Additional feature would be to check if start and end points are not same
#and the numbers are greater than zero.

x_grid = int(input("How many grid points in x-direction? \n"))
y_grid = int(input("How many grid points in y-direction? \n"))
points = x_grid * y_grid

start_point_x = int(input("x-coord of start? (0 to " + str(x_grid-1) + ")\n"))
start_point_y = int(input("y-coord of start? (0 to " + str(y_grid-1) + ")\n"))
start_loc = [start_point_x,start_point_y]

end_point_x = int(input("x-coord of end? (0 to " + str(x_grid-1) + ")\n"))
end_point_y = int(input("y-coord of end? (0 to " + str(y_grid-1) + ")\n"))
end_loc = [end_point_x,end_point_y]

obstacles = int(input("number of obstacles? (0 to " + str(points - 2) + ")\n"))

#Begin matrix grid mapping.
matrix = []

for y in range(x_grid):
  matrix_row = []

  for x in range(y_grid):
    matrix_row.append(1)
  matrix.append(matrix_row)
print(matrix)

#Add locations of starting/end points.
obstacles_loc = []
obstacles_loc.append(start_loc)
obstacles_loc.append(end_loc)

#Add a new obstacle in random locations of available points.
i = 0

while i < obstacles:
  new_obs_x = random.randint(0,x_grid-1)
  new_obs_y = random.randint(0,y_grid-1)

  if [new_obs_x,new_obs_y] in obstacles_loc:
    print("Obstacle overlap!")
  else:
    matrix[new_obs_x][new_obs_y] = 0
    obstacles_loc.append([new_obs_x,new_obs_y])
    i += 1

print("List of obstacle locations: " + str(obstacles_loc))
print("Matrix grid layout:" + str(matrix))

#Assess whether path is reachable with current grid layout.

#If delivery fails, select the 1st obstacle in the obstacle list to remove
#and overwrite the obstacle location with a 1 to become free space
#Then repeat the procedure using the new grid.

delivered = False
while not delivered:
  path_length = assess_route(matrix, start_loc, end_loc)

  if path_length == 0:
    print("Unable to reach delivery spot")
    replace_x = int(obstacles_loc[2][0])
    replace_y = int(obstacles_loc[2][1])
    matrix[replace_x][replace_y] = 1
    obstacles_loc.pop(2)
    print(obstacles_loc)
    print("Repeat attempt")
  else:
    delivered = True
    print("Reached Location!!")