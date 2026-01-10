# black jack in python wth pygame!
import copy
import random
import pygame
import traceback
import time

pygame.init()
#variables [DN] dit is geen nuttige comment, het is een game, dus je zegt 'variables' iedereen kan dat zien door de code te lezen. 
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
cached_scaled_surface = None # [DN] waarom begint deze met een _ ?

button_Y_coordinate = 820
button_height = 50

CARD_WIDTH = 120
CARD_HEIGHT = 220
CARD_X_OFFSET = 70
CARD_Y_OFFSET_PLAYER = 460
CARD_Y_OFFSET_DEALER = 160
CARD_SPACING_X = 70
CARD_SPACING_Y = 5

TEXT_LEFT_X = 5
TEXT_RIGHT_X = 80
TEXT_TOP_Y = 5
TEXT_BOTTOM_Y = 175

BORDER_RADIUS = 5
BORDER_WIDTH = 3
CARD_COLOR = 'white'
BORDER_COLOR = 'grey20'
TEXT_COLOR = 'black'


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
round_resolved = False

#outcome codes and results
results = ['', 'PLAYER BUSTED O_o', 'YOU WIN! :D', 'DEALER WINS :(', 'TIE GAME...']
OUT_BUST = 1
OUT_WIN = 2
OUT_LOSS = 3
OUT_PUSH = 4
OUT_BLACKJACK = 5
#mapping labels to outcome codes
RESULT_LABELS = {
    OUT_BUST: "Bust",
    OUT_WIN: "Win",
    OUT_LOSS: "Loss",
    OUT_PUSH: "Push",
    OUT_BLACKJACK: "Blackjack"
}

#betting variables
bankroll = 1000
current_bet = 0
stake_reserved = 0
bet_locked = False
MIN_BET = 10
MAX_BET = 10000

chip_buttons = { # [DN] je kan dit korter schrijven, de x coordinate is altijd + 85, de rest blijft hetzelfde. Gebruik ofwel een loop, of gebruik vriabelen voor 820 of 50. Zo moet je het maar op 1 plek aanpassen als je het later moet veranderen
    10: pygame.Rect(50, button_Y_coordinate, 80, button_height),
    50: pygame.Rect(135, button_Y_coordinate, 80, button_height),
    100: pygame.Rect(220, button_Y_coordinate, 100, button_height),
    500: pygame.Rect(325, button_Y_coordinate, 100, button_height),
}

clear_button = pygame.Rect(430, button_Y_coordinate, 150, button_height)
all_in_button = pygame.Rect(585, button_Y_coordinate, 140, button_height)
placebet_button = pygame.Rect(730, button_Y_coordinate, 220, button_height)


# betting functions
def change_bet(amount):
    global current_bet, bankroll  # [DN] niet zeker waarom je hier global gebruikt, maar ook veel variabelen bovenaan declareert. Maakt niet zoveel uit wat je kiest, het belangrijkste is 
    if bet_locked:
        return
    current_bet = min(bankroll, max(0, current_bet + amount))


def confirm_place_bet():
    global bankroll, current_bet, stake_reserved, bet_locked
    # require a positive bet that does not exceed bankroll
    if current_bet >= MIN_BET and current_bet <= bankroll and bankroll > 0:
        stake_reserved = int(current_bet)
        bankroll -= stake_reserved      # reserve stake from bankroll
        bet_locked = True
        current_bet = 0                 # clear bet now that it's reserved [DN] vreemd dat je begint over de UI hier, dit lijkt code over het spel. Architectuur is normaalgezien dat UI alles ziet, maar de 'echte' functionaliteit niet weet dat ui bestaat. Dit is 2de jaars kennis, mvvm gewoon dat je weet dat het bestaat
        
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
    if stake_reserved <= 0:
        bet_locked = False
        stake_reserved = 0
        return
    stake = int(stake_reserved)
    #result values: 1-bust, 2-win, 3-loss, 4-push, 5-blackjack
    if result == OUT_WIN:
        bankroll += stake * 2 #player win -> bet x2
    elif result == OUT_BLACKJACK:
        bankroll += int(stake * 2.5) #blackjack payout 3:2
    elif result == OUT_PUSH:
        bankroll += stake    #push, return bet
    else:
       
        stake_reserved = 0
    bet_locked = False    


def resolve_round():
    global outcome, dealer_score, player_score, hand_active, reveal_dealer
    player_score = calculate_score(my_hand)
    dealer_score = calculate_score(dealer_hand)
    # different outcomes based on result value (1 bust, 2 win, 3 loss, 4 push, 5 blackjack)
    if player_score > 21:
        outcome = OUT_BUST
    elif dealer_score > 21:
        outcome = OUT_WIN
    elif player_score == dealer_score:
        outcome = OUT_PUSH
    elif player_score == 21 and len(my_hand) == 2 and not (dealer_score == 21 and len(dealer_hand) == 2):
        outcome = OUT_BLACKJACK            
    elif player_score > dealer_score:
        outcome = OUT_WIN
    else:
        outcome = OUT_LOSS
    
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


def draw_cards(player, dealer, reveal):
     # [DN] zelfde remark, ik denk dat je heel veel herhaling hebt die je minstens in variabelen kunt steken, 
    for i, card in enumerate(player):
        x = CARD_X_OFFSET + CARD_SPACING_X * i
        y = CARD_Y_OFFSET_PLAYER + CARD_SPACING_Y * i

        pygame.draw.rect(logical_surface, CARD_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), 0, BORDER_RADIUS)

        logical_surface.blit(font.render(card, True, TEXT_COLOR), (x + TEXT_LEFT_X, y + TEXT_TOP_Y))
        logical_surface.blit(font.render(card, True, TEXT_COLOR), (x + TEXT_LEFT_X, y + TEXT_BOTTOM_Y))
        logical_surface.blit(font.render(card, True, TEXT_COLOR), (x + TEXT_RIGHT_X, y + TEXT_TOP_Y))
        logical_surface.blit(font.render(card, True, TEXT_COLOR), (x + TEXT_RIGHT_X, y + TEXT_BOTTOM_Y))

        pygame.draw.rect(logical_surface, BORDER_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), BORDER_WIDTH, BORDER_RADIUS)

    for i, card in enumerate(dealer):
        x = CARD_X_OFFSET + CARD_SPACING_X * i
        y = CARD_Y_OFFSET_DEALER + CARD_SPACING_Y * i

        pygame.draw.rect(logical_surface, CARD_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), 0, BORDER_RADIUS)

        display = card if i != 0 or reveal else '???'

        logical_surface.blit(font.render(display, True, TEXT_COLOR), (x + TEXT_LEFT_X, y + TEXT_TOP_Y))
        logical_surface.blit(font.render(display, True, TEXT_COLOR), (x + TEXT_LEFT_X, y + TEXT_BOTTOM_Y))
        logical_surface.blit(font.render(card, True, TEXT_COLOR), (x + TEXT_RIGHT_X, y + TEXT_TOP_Y))
        logical_surface.blit(font.render(card, True, TEXT_COLOR), (x + TEXT_RIGHT_X, y + TEXT_BOTTOM_Y))

        pygame.draw.rect(logical_surface, BORDER_COLOR, (x, y, CARD_WIDTH, CARD_HEIGHT), BORDER_WIDTH, BORDER_RADIUS)

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
        # show final/all-in hint when a stake is reserved (bet_locked) even if bankroll == 0
        if bet_locked and stake_reserved > 0 and bankroll <= 0:
            logical_surface.blit(font.render('Last $$$, final hand in progress!', True, 'yellow'), (100, 400))
        # only show Game Over when there is no reserved stake and no active bet
        elif bankroll <= 0 and not bet_locked and stake_reserved <= 0:
            logical_surface.blit(smaller_font.render('You are out of money! Restart the game to play again.', True, 'white'), (100, 400))
     #safe retrieve result label       
    label = RESULT_LABELS.get(result, 'Unknown Result')        
    logical_surface.blit(font.render(label, True, 'white'), (550, 25))
    
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
        label = RESULT_LABELS.get(result, "Unknown result")
        logical_surface.blit(font.render(label, True, 'white'), (15, 25))
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
    try:
        # run game at our framerate and fill screen with bg color
        timer.tick(fps)
        logical_surface.fill('grey45')

        
        # check bankroll, if 0 disable game start
        if not active and bankroll <= 0 and not bet_locked and (stake_reserved <= 0):
            logical_surface.blit(smaller_font.render('You are out of money! Restart the game to play again.', True, 'white'), (100, 400))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            buttons = draw_game(active, records, outcome)
            pygame.display.update()            
            continue

        # initial deal to player and dealer
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False

            player_score = calculate_score(my_hand)
            dealer_score = calculate_score(dealer_hand)
            if player_score == 21 and len(my_hand) == 2:
                reveal_dealer = True
                hand_active = False
                resolve_round()
                round_resolved = True
        # once game is activated, and dealt, calculate scores and display cards
        if active:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            # if player busts immediately reveal dealer to trigger round resolution
            if player_score > 21 and hand_active:
                reveal_dealer = True
                hand_active = False

            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                else:
                    if not round_resolved and not hand_active:
                        resolve_round()
                        round_resolved = True

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
                        # only allow start hand if bet placed
                        if not active and bet_locked and stake_reserved > 0:
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
                            hand_active = False
                            reveal_dealer = False
                            add_score = True
                            dealer_score = 0
                            player_score = 0

                            stake_reserved = 0
                            bet_locked = False
                            current_bet = 0

                            round_resolved = False





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

    except Exception:
        exception_info = traceback.format_exc()
        print("An error occurred:\n", exception_info)

        err_lines = exception_info.splitlines()[-6:]  # Get last 6 lines of the traceback
        logical_surface.fill('black')
        y = 40
        for line in err_lines:
            try: 
                logical_surface.blit(smaller_font.render(line[:120], True, 'red'), (20, y))
            except Exception:
                pass
            y += 24    
        logical_surface.blit(smaller_font.render("See console for full traceback.", True, 'red'), (20, y + 8))    

        dx = 20
        dy = 20
        for line in DEBUG_LINES:
            try:
                logical_surface.blit(smaller_font.render(line[:120], True, 'yellow'), (WIDTH - 400 + dx, dy))
            except Exception:
                pass
            dy += 18
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break 
            time.sleep(0.1)  
            if not run:
                break
pygame.quit()
