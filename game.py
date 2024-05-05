import pygame
import sys
from random import choice, randint

class Gopal(pygame.sprite.Sprite):
    def __init__(self, position, constraint, velocity):
        super().__init__()
        self.image = pygame.image.load('./Assets/gopal.png')
        self.rect = self.image.get_rect(midbottom=position)
        self.velocity = velocity
        self.xconstraint = constraint
        self.ready = True
        self.cookie_time = 0
        self.cookie_cooldown = 600

        self.cookies = pygame.sprite.Group()

        self.cookie_sound = pygame.mixer.Sound('./Assets/cookie_sound.wav')
        self.cookie_sound.set_volume(0.5)

    def move_gopal(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_cookie()
            self.ready = False
            self.cookie_time = pygame.time.get_ticks()
            self.cookie_sound.play()

    def recharge_cookie(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.cookie_time >= self.cookie_cooldown:
                self.ready = True

    def boundary_check(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.xconstraint:
            self.rect.right = self.xconstraint

    def shoot_cookie(self):
        self.cookies.add(Cookie(self.rect.center, -8, self.rect.bottom, 'brown'))

    def update(self):
        self.move_gopal()
        self.boundary_check()
        self.recharge_cookie()
        self.cookies.update()

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, velocity, screen_height, color):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect(midbottom=pos)
        self.velocity = velocity
        self.y_constraint = screen_height

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y <= -50 or self.rect.y >= self.y_constraint + 50:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = color + '.png'
        self.image = pygame.image.load('./Assets/' + file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        if color == 'koko_jumbo':
            self.value = 100
        elif color == 'prob':
            self.value = 200
        else:
            self.value = 300

        self.laser_cooldown = randint(1000, 3000)
        self.last_shoot_time = pygame.time.get_ticks()

    def update(self, direction):
        self.rect.x += direction

    def shoot_laser(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.laser_cooldown:
            self.last_shoot_time = current_time
            return True
        return False

class Cookie(pygame.sprite.Sprite):
    def __init__(self, pos, velocity, screen_height, color):
        super().__init__()
        self.image = pygame.image.load('./Assets/cookie.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.velocity = velocity
        self.y_constraint = screen_height

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y <= -50 or self.rect.y >= self.y_constraint + 50:
            self.kill()

class GoopalCookies:
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 700
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load('./Assets/background.jpeg').convert_alpha()

        self.player = pygame.sprite.GroupSingle(Gopal(
            (self.screen_width / 2, self.screen_height), self.screen_width, 5))

        self.lives = 3
        self.lives_surf = pygame.image.load('./Assets/lives.png').convert_alpha()
        self.lives_x_start_pos = self.screen_width - \
            (self.lives_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('./Assets/m04.TTF', 20)

        self.enemies = pygame.sprite.Group()
        self.enemy_lasers = pygame.sprite.Group()
        self.setup_enemies(rows=3, cols=6)
        self.enemy_direction = 1

        self.music = pygame.mixer.Sound('./Assets/music.wav')
        self.music.set_volume(0.5)
        self.laser_sound = pygame.mixer.Sound('./Assets/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('./Assets/explosion.wav')
        self.explosion_sound.set_volume(0.5)

    def setup_enemies(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=50):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    enemy_sprite = Enemy('adudu', x, y)
                elif row_index == 1:
                    enemy_sprite = Enemy('prob', x, y)
                elif row_index == 2:
                    enemy_sprite = Enemy('koko_jumbo', x, y)
                self.enemies.add(enemy_sprite)

    def enemy_position_check(self):
        all_enemies = self.enemies.sprites()
        for enemy in all_enemies:
            if enemy.rect.right >= self.screen_width:
                self.enemy_direction = -1
                self.enemy_move_down(2)
            elif enemy.rect.left <= 0:
                self.enemy_direction = 1
                self.enemy_move_down(2)

    def enemy_move_down(self, distance):
        if self.enemies:
            for enemy in self.enemies.sprites():
                enemy.rect.y += distance

    def enemy_shoot_laser(self):
        for enemy in self.enemies:
            if enemy.shoot_laser():
                laser_sprite = Laser(enemy.rect.center,
                                     10, self.screen_height, 'green')
                self.enemy_lasers.add(laser_sprite)
                self.laser_sound.play()

    def collision_detection(self):
        for cookie in self.player.sprite.cookies:
            enemies_hit = pygame.sprite.spritecollide(cookie, self.enemies, True)
            for enemy in enemies_hit:
                self.score += enemy.value
                cookie.kill()
                self.explosion_sound.play()

        for laser in self.enemy_lasers:
            if pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                self.lives -= 1

        for enemy in self.enemies:
            if pygame.sprite.spritecollide(enemy, self.player, False):
                pygame.quit()
                sys.exit()

    def display_lives(self):
        for live in range(self.lives):
            x = self.lives_x_start_pos + \
                ((live-1) * (self.lives_surf.get_size()[0] + 10))
            self.screen.blit(self.lives_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 10))
        self.screen.blit(score_surf, score_rect)

    def game_result(self):
        if not self.enemies.sprites():
            victory_surf = self.font.render(
                'Selamat! Anda Menang', False, 'white')
            victory_rect = victory_surf.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2))
            self.screen.blit(victory_surf, victory_rect)
            self.menu_retry_victory()
            pygame.display.update()

        if self.lives <= 0:
            self.menu_retry_defeat()

    def menu_retry_victory(self):
        retry_img = pygame.image.load('./Assets/retry.png').convert_alpha()
        exit_img = pygame.image.load('./Assets/exit.png').convert_alpha()

        retry_button = Button((self.screen_width / 2), 590, retry_img, 0.8)
        exit_button = Button((self.screen_width / 2), 650, exit_img, 0.8)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if retry_button.draw(self.screen):
                self.reset_game()
                break

            if exit_button.draw(self.screen):
                pygame.quit()
                sys.exit()

            pygame.display.update()

    def menu_retry_defeat(self):
        retry_img = pygame.image.load('./Assets/retry.png').convert_alpha()
        exit_img = pygame.image.load('./Assets/exit.png').convert_alpha()

        retry_button = Button((self.screen_width / 2), 590, retry_img, 0.8)
        exit_button = Button((self.screen_width / 2), 650, exit_img, 0.8)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if retry_button.draw(self.screen):
                self.reset_game()
                break

            if exit_button.draw(self.screen):
                pygame.quit()
                sys.exit()

            pygame.display.update()

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.player.sprite.rect.midbottom = (self.screen_width / 2, self.screen_height)
        self.enemies.empty()
        self.enemy_lasers.empty()
        self.setup_enemies(rows=3, cols=6)
        self.enemy_direction = 1

    def run(self):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.screen.blit(self.background, (0, 0))

        self.player.update()
        self.enemy_shoot_laser()
        self.enemy_lasers.update()

        self.enemies.update(self.enemy_direction)
        self.enemy_position_check()
        self.collision_detection()

        self.player.sprite.cookies.draw(self.screen)
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemy_lasers.draw(self.screen)
        self.display_lives()
        self.display_score()
        self.game_result()

        pygame.display.flip()
        self.clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    game = GoopalCookies()
    pygame.display.set_caption("Gopal-Cookies")
    while True:
        game.run()
