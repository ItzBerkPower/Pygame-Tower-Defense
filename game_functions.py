from tower import Tower

def refund_money(money, all_towers):
    upgrade_prices = { # Dictionary with all the prices of every tower upgrade
        'turret1': [0, 100, 125, 150],
        'turret2': [0, 200, 250, 300],
        'turret3': [0, 400, 500]
    }

    # Refunding the money for the towers, by looping through all the towers
    for tower in all_towers:
        # Add the cost of the upgrades, plus the initial cost of the tower
        money += upgrade_prices[tower.turret_type][tower.upgrade_level - 1] + upgrade_prices[tower.turret_type][1]
                        
    all_towers.clear() # Clear all the towers from the list
    return money


def side_menu(screen, side_menu_open, side_menu_image, side_menu_small_image, mouse_x):

    if side_menu_open:
        side_menu_rect = side_menu_image.get_rect()
        side_menu_rect.topleft = (300, 0)
        screen.blit(side_menu_image, side_menu_rect)

        if mouse_x < 370:
            side_menu_open = False

    if not side_menu_open:
        menu_rect = side_menu_small_image.get_rect()
        menu_rect.topleft = (700, 0)
        screen.blit(side_menu_small_image, menu_rect)

        if mouse_x > 700:
            side_menu_open = True
    
    return side_menu_open



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

