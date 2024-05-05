import pygame
from game import GoopalCookies, Button

def main_menu():
    pygame.init()
    pygame.mixer.init()

    game = GoopalCookies()
    pygame.display.set_caption("Gopal-Cookies")

    enemy_imageblue = pygame.image.load('./Assets/Adudu.png').convert_alpha()
    enemy_imageorange = pygame.image.load('./Assets/Prob.png').convert_alpha()
    enemy_imagegreen = pygame.image.load('./Assets/Koko_jumbo.png').convert_alpha()
    scoreo = game.font.render('100', True, 'black')
    scoreg = game.font.render('200', True, 'black')
    scoreb = game.font.render('300', True, 'black')
    scoreoRect = scoreo.get_rect()
    scoregRect = scoreg.get_rect()
    scorebRect = scoreb.get_rect()

    scoreE = game.font.render('SCORE', True, 'black')
    scoreERect = scoreE.get_rect()

    logo_img = pygame.image.load('./Assets/mainlogo.png').convert_alpha()
    start_img = pygame.image.load('./Assets/start.png').convert_alpha()
    exit_img = pygame.image.load('./Assets/exit.png').convert_alpha()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.screen.blit(game.background,(0,0))
        game.screen.blit(logo_img,(50,10))
        game.screen.blit(enemy_imageorange,((game.screen_width/2)+50,game.screen_height/2))
        game.screen.blit(enemy_imagegreen,((game.screen_width/2)+50,(game.screen_height/2)+50))
        game.screen.blit(enemy_imageblue,((game.screen_width/2)+50,(game.screen_height/2)+100))
        game.screen.blit(scoreo,((game.screen_width/2)-90, (game.screen_height/2)+10))
        game.screen.blit(scoreg,((game.screen_width/2)-90,(game.screen_height/2)+60))
        game.screen.blit(scoreb,((game.screen_width/2)-90,(game.screen_height/2)+110))
        game.screen.blit(scoreE,((game.screen_width/2)-90, (game.screen_height/2)-30))

        start_button = Button((game.screen_width/2), 590, start_img, 0.8)
        exit_button = Button((game.screen_width/2), 650, exit_img, 0.8)

        if start_button.draw(game.screen):
            game.reset_game()
            game_loop(game)
        if exit_button.draw(game.screen):
            run = False

        pygame.display.update()

    pygame.quit()

def game_loop(game):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        game.run()

if __name__ == '__main__':
    main_menu()
