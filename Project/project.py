# black jack in python wth pygame!
import copy
import random
import pygame

pygame.init()
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH, HEIGHT = 1200, 900
LOGICAL_SIZE = (1200, 900)
logical_surface = pygame.Surface(LOGICAL_SIZE)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
_cached_scaled_surface = None

# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'PLAYER BUSTED O_o', 'YOU WIN! :D', 'DEALER WINS :(', 'TIE GAME...']

#betting variables
bankroll = 1000
current_bet = 0
stake_reserved = 0
bet_locked = False
MIN_BET = 10
MAX_BET = 10000

chip_buttons = {
    10: pygame.Rect(50, 820, 80, 50),
    50: pygame.Rect(135, 820, 80, 50),
    100: pygame.Rect(220, 820, 100, 50),
    500: pygame.Rect(325, 820, 100, 50),
}
clear_button = pygame.Rect(430, 820, 150, 50)
all_in_button = pygame.Rect(585, 820, 140, 50)
placebet_button = pygame.Rect(730, 820, 220, 50)

# betting functions
def change_bet(amount):
    global current_bet, bankroll
    if bet_locked:
        return
    new_bet = current_bet + amount
    new_bet = max(0, new_bet)
    new_bet = min(bankroll, new_bet)
    current_bet = new_bet

def confirm_place_bet():
    global bankroll, current_bet, stake_reserved, bet_locked
    # require a positive bet that does not exceed bankroll
    if current_bet >= MIN_BET and current_bet <= bankroll and bankroll > 0:
        stake_reserved = int(current_bet)
        bankroll -= stake_reserved      # remove stake from bankroll immediately
        bet_locked = True
        current_bet = 0                 # clear UI bet now that it's reserved
        return True
    return False


def clear_bet():
    global current_bet
    if bet_locked:
        return
    current_bet = 0


def all_in():
    global current_bet, bankroll
    if bet_locked:
        return
    current_bet = bankroll   

#Betting payout function
def payout(result):
    global bankroll, stake_reserved, bet_locked
    #nothing reserved -> safe exit
    if current_bet <= 0:
        bet_locked = False
        stake_reserved = 0
        return
    stake = int(stake_reserved)
    #result values: 1-bust, 2-win, 3-loss, 4-push, 5-blackjack
    if result == 2:
        bankroll += stake * 2 #player win -> bet x2
    elif result == 5:
        bankroll += int(stake * 2.5) #blackjack payout 3:2
    elif result == 4:
        bankroll += stake    #push, return bet
    #reset bet
    stake_reserved = 0
    bet_locked = False    

def resolve_round(result):
    global outcome, add_score, dealer_score, player_score, hand_active, reveal_dealer
    player_score = calculate_score(my_hand)
    dealer_score = calculate_score(dealer_hand)
    # different outcomes based on result value (1 bust, 2 win, 3 loss, 4 push, 5 blackjack)
    if player_score > 21:
        outcome = 1
    elif dealer_score > 21:
        outcome = 2
    elif player_score == dealer_score:
        outcome = 4
    elif player_score == 21 and len(my_hand) == 2 and not (dealer_score == 21 and len(dealer_hand) == 2):
        outcome = 5            
    elif player_score > dealer_score:
        outcome = 2
    else:
        outcome = 3
    
    payout(outcome)    
    
    #freeze hand state
    hand_active = False 
    reveal_dealer = True

# get scale factors for logical to screen size conversion
def screen_to_logical(pos):
    sw, sh = screen.get_size()
    lw, lh = LOGICAL_SIZE
    scale = min(sw / lw, sh / lh)
    target_w, target_h = int(lw * scale), int(lh * scale)
    x_offset = (sw - target_w) // 2
    y_offset = (sh - target_h) // 2
    sx, sy = pos
    lx = (sx - x_offset) / scale
    ly = (sy - y_offset) / scale
    return int(lx), int(ly)


# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card - 1)
    return current_hand, current_deck


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    logical_surface.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    if reveal_dealer:
        logical_surface.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))


# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(logical_surface, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        logical_surface.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        logical_surface.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        logical_surface.blit(font.render(player[i], True, 'black'), (150 + 70 * i, 465 + 5 * i))
        logical_surface.blit(font.render(player[i], True, 'black'), (150 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(logical_surface, 'grey20', [70 + (70 * i), 460 + (5 * i), 120, 220], 3, 5)

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(logical_surface, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            logical_surface.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            logical_surface.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
            logical_surface.blit(font.render(dealer[i], True, 'black'), (150 + 70 * i, 165 + 5 * i))
            logical_surface.blit(font.render(dealer[i], True, 'black'), (150 + 70 * i, 335 + 5 * i))
        else:
            logical_surface.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            logical_surface.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
            logical_surface.blit(font.render(dealer[i], True, 'black'), (150 + 70 * i, 165 + 5 * i))
            logical_surface.blit(font.render(dealer[i], True, 'black'), (150 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(logical_surface, 'grey20', [70 + (70 * i), 160 + (5 * i), 120, 220], 3, 5)


# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2,3,4,5,6,7,8,9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score


# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    if not act:
        if bankroll <= 0:
            logical_surface.blit(font.render('You are out of money! Restart the game to play again.', True, 'white'), (100, 400))
    
    # initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(logical_surface, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(logical_surface, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        logical_surface.blit(deal_text, (165, 50))
        button_list.append(deal)
        #betting display
        logical_surface.blit(smaller_font.render(f'Bankroll: ${bankroll}', True, 'white'), (50, 750))
        logical_surface.blit(smaller_font.render(f'Current Bet: ${current_bet}', True, 'white'), (50, 780))
        #draw chip buttons
        pygame.draw.rect(logical_surface, 'gold', chip_buttons[10], 0, 5)
        logical_surface.blit(smaller_font.render('$10', True, 'black'), (chip_buttons[10].x + 15, chip_buttons[10].y + 10))
        pygame.draw.rect(logical_surface, 'gold', chip_buttons[50], 0, 5)
        logical_surface.blit(smaller_font.render('$50', True, 'black'), (chip_buttons[50].x + 15, chip_buttons[50].y + 10))
        pygame.draw.rect(logical_surface, 'gold', chip_buttons[100], 0, 5)
        logical_surface.blit(smaller_font.render('$100', True, 'black'), (chip_buttons[100].x + 10, chip_buttons[100].y + 10))
        pygame.draw.rect(logical_surface, 'gold', chip_buttons[500], 0, 5)
        logical_surface.blit(smaller_font.render('$500', True, 'black'), (chip_buttons[500].x + 10, chip_buttons[500].y + 10))
        # clear, all in and place bet buttons
        pygame.draw.rect(logical_surface, 'red', clear_button, 0, 5)
        logical_surface.blit(smaller_font.render('CLEAR', True, 'black'), (clear_button.x + 10, clear_button.y + 10))  
        pygame.draw.rect(logical_surface, 'red', all_in_button, 0, 5)
        logical_surface.blit(smaller_font.render('ALL IN', True, 'black'), (all_in_button.x + 10, all_in_button.y + 10))  
        pygame.draw.rect(logical_surface, 'green', placebet_button, 0, 5)
        logical_surface.blit(smaller_font.render('PLACE BET', True, 'black'), (placebet_button.x + 10, placebet_button.y + 10)) 
        button_list.extend([chip_buttons[10], chip_buttons[50], chip_buttons[100], chip_buttons[500], clear_button, all_in_button, placebet_button])
        # bet button (greyed out if no/too small bet placed)   
        place_bet_color = 'springgreen' if current_bet >= MIN_BET else 'grey50'
        pygame.draw.rect(logical_surface, place_bet_color, placebet_button, 0, 5)
        logical_surface.blit(smaller_font.render('PLACE BET', True, 'black'), (placebet_button.x + 10, placebet_button.y + 10))
        
    # once game started, show hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(logical_surface, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(logical_surface, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        logical_surface.blit(hit_text, (73, 730))
        button_list.append(hit)
        stand = pygame.draw.rect(logical_surface, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(logical_surface, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        logical_surface.blit(stand_text, (368, 730))
        button_list.append(stand)
        score_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        logical_surface.blit(score_text, (40, 840))
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        logical_surface.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(logical_surface, 'white', [75, 280, 450, 250], 0, 5)
        pygame.draw.rect(logical_surface, 'green', [75, 280, 450, 250], 3, 5)
        pygame.draw.rect(logical_surface, 'black', [78, 283, 444, 244], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        logical_surface.blit(deal_text, (165, 380))
        button_list.append(deal)
    return button_list


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push, 5-blackjack
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        elif play_score == 21 and len(my_hand) == 2 and not (dealer_score == 21 and len(dealer_hand) == 2):
            result = 5
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


# main game loop
run = True
_cached_scaled_surface = None

while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    logical_surface.fill('grey45')
    
    # check bankroll, if 0 disable game start
    if bankroll <= 0:
        logical_surface.blit(font.render('You are out of money! Restart the game to play again.', True, 'white'), (100, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        continue

    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            else:
                if hand_active:
                    resolve_round()    
        draw_scores(player_score, dealer_score)
    buttons = draw_game(active, records, outcome)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # update screen size if window resized    
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

        elif event.type == pygame.MOUSEBUTTONUP:
            logical_pos = screen_to_logical(event.pos)
            if logical_pos is None:
                continue
            # if table not active, allow betting UI + deal/new hand
            if not active:
                # Betting UI
                if not bet_locked:
                    for chip_value, chip_rect in chip_buttons.items():
                        if chip_rect.collidepoint(logical_pos):
                            change_bet(int(chip_value))
                            break
                # check clear, all in and place bet buttons
                if clear_button.collidepoint(logical_pos):
                    clear_bet()
                elif all_in_button.collidepoint(logical_pos) and bankroll > 0:
                    all_in()
                elif placebet_button.collidepoint(logical_pos):
                    if confirm_place_bet():
                        pass  # bet placed successfully
                    else:
                        pass  # do nothing if bet not valid    
                else: #bet_locked is True -> stake reserved, player must press deal to start hand
                    pass     

                # deal new hand button
                if buttons and buttons[0].collidepoint(logical_pos):
                    if bet_locked and not active and stake_reserved > 0:
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                        dealer_score = 0
                        player_score = 0    
                    else: #ignore or show message if no bet placed
                        pass    
            else:
                # if player can hit, allow them to draw a card
                if buttons and buttons[0].collidepoint(logical_pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # allow player to end turn (stand)
                elif len(buttons) > 1 and buttons[1].collidepoint(logical_pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                # allow player to start new hand after win/loss/push
                elif len(buttons) == 3 and buttons[2].collidepoint(logical_pos):
                        # don't allow new hand unless bet placed
                        active = False
                        initial_deal = False
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                        dealer_score = 0
                        player_score = 0

                        stake_reserved = 0
                        bet_locked = False
                        current_bet = 0



    # if player busts, automatically end turn - treat like a stand
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    # scale logical surface to fit screen while maintaining aspect ratio
    sw, sh = screen.get_size()
    lw, lh = LOGICAL_SIZE
    scale = min(sw / lw, sh / lh)
    target_size = (int(lw * scale), int(lh * scale))

    _cached_scaled_surface = pygame.transform.smoothscale(logical_surface, (target_size))

    screen.fill((0, 0, 0))
    x_offset = (sw - target_size[0]) // 2
    y_offset = (sh - target_size[1]) // 2
    screen.blit(_cached_scaled_surface, (x_offset, y_offset))
    pygame.display.flip()

pygame.quit()