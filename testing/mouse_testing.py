
# FUNCTION TO TEST: Picking a tower

# Pick the tower
def pick_tower(side_menu_open, x, y, money, picked_tower):
    # If the side menu open and the player clicked on the correct x-range for a button
    if side_menu_open and x in range(430,615):

        # If clicked first button, and enough money
        if y in range(125, 180) and money >= 100:
            picked_tower = "turret1" # Pick the turret
            money -= 100 # Take away money
                            
        elif y in range(275, 330) and money >= 200:
            picked_tower = "turret2" # Pick the turret
            money -= 200 # Take away money

        elif y in range(430, 480) and money >= 400:
            picked_tower = "turret3" # Pick the turret
            money -= 400 # Take away money
    
    # Return the variables changed
    return money, picked_tower

# Mouse coordinates: (445, 150)
money, picked_tower = pick_tower(side_menu_open, 445, 150, money, picked_tower)
# Output: Picked turret 1 (Expected)

# Mouse coordinates: (630, 125)
money, picked_tower = pick_tower(side_menu_open, 630, 125, money, picked_tower)
# Output: No tower was picked (Expected)

# Mouse coordinates: (610, 500)
money, picked_tower = pick_tower(side_menu_open, 610, 500, money, picked_tower)
# Output: No tower was picked (Expected)

# Overall comments: Passed all tests as expected
