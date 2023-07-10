import random
import typing

    print("INFO")

    return {
        "apiversion": "1",
        "author": "Emily",  # TODO: Your Battlesnake Username
        "color": "#A020F0",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    #print(game_state['you']['body'])

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    #for left and right borders
    if my_head["x"] ==0:  # head is at left, dont move left
        is_move_safe["left"] = False
    elif my_head["x"] == board_width-1:  # head is at right, dont move right
        is_move_safe["right"] = False

    #for top and bottom borders NEW IF NEEDED NOT JUST ANOTHER ELIF
    if my_head["y"] ==0:  # head is at bottom, dont move down
        is_move_safe["down"] = False
    elif my_head["y"] == board_height-1:  # head is at top, dont move up
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    for body_part in my_body:
      #left
      if{'x':my_head['x']-1, 'y':my_head['y']}==body_part:
        is_move_safe['left']=False
      #right
      if{'x':my_head['x']+1, 'y':my_head['y']}==body_part:
        is_move_safe['right']=False
      #up
      if{'x':my_head['x'], 'y':my_head['y']+1}==body_part:
        is_move_safe['up']=False
      #down
      if{'x':my_head['x'], 'y':my_head['y']-1}==body_part:
        is_move_safe['down']=False
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for enemy_snakes in opponents:
      for body_part in enemy_snakes['body']:
        #left
        if{'x':my_head['x']-1, 'y':my_head['y']}==body_part:
          is_move_safe['left']=False
        #right
        if{'x':my_head['x']+1, 'y':my_head['y']}==body_part:
          is_move_safe['right']=False
        #up
        if{'x':my_head['x'], 'y':my_head['y']+1}==body_part:
          is_move_safe['up']=False
        #down
        if{'x':my_head['x'], 'y':my_head['y']-1}==body_part:
          is_move_safe['down']=False
  
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    #food = game_state['board']['food']
    #largest_opponent=0;
    #for enemy_snakes in opponents:
      #if enemy_snakes['length']>largest_opponent:
        #largest_opponent=enemy_snakes['length']

#or game_state["you"]["length"]<=largest_opponent

    if game_state["you"]["health"]<70 or game_state['turn']<9:
      print(f"want food")
      # Calculate distance between our Battlesnake's head and each piece of food on the board
      food_distances = []
      for food in game_state['board']['food']:
          food_distance = abs(my_head['x'] - food["x"]) + abs(my_head['y'] - food["y"])
          food_distances.append(food_distance)
  
      # Choose the food that is closest to our Battlesnake's head
      closest_food_index = food_distances.index(min(food_distances))
      closest_food = game_state["board"]["food"][closest_food_index]
  
      # Move towards the closest food
      if closest_food["x"] > my_head['x']:
        if is_move_safe["right"]==True:
          #print(f"made it to closet food turn right")
          #print(closest_food["x"])
          next_move= "right"
      elif closest_food["x"] < my_head['x']:
        if is_move_safe["left"]==True:
          #print(f"made it to closet food turn left")
          #print(closest_food["x"])
          next_move= "left"
      elif closest_food["x"] == my_head['x']:
        if closest_food["y"] < my_head['y']:
          if is_move_safe["down"]==True:
            #print(f"made it to closet food turn down")
            #print(closest_food["y"])
            #print(my_head['y'])
            next_move= "down"
        elif closest_food["y"] > my_head['y']:
          if is_move_safe["up"]==True:
            #print(f"made it to closet food turn up")
            #print(closest_food["y"])
            next_move= "up"
  
  
    #TO THINK ON- THINK AHEAD- SNAKE WILL RUN ITSELF INTO A TIGHT SPACE BECAUSE IT IS AN IDIOT
  
    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
