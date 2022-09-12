import pygame
from Game import Game
from Ball import Ball
from Paddle import Paddle
import neat
import pickle

class NEATGAME:
    def __init__(self, window, width,height):
        self.game = Game(window, width,height)
        self.ball = self.game.ball
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle


    def calculate_fitness(self,game_info):
        self.genome1.fitness += game_info.left_hits 
        self.genome2.fitness += game_info.right_hits 

    def test_ai(self, winner_net):

        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP] and self.right_paddle.y - Paddle.VEL >= 0:
                self.right_paddle.move(up = True)

            if keys[pygame.K_DOWN] and self.right_paddle.y + self.right_paddle.HEIGHT + Paddle.VEL <= 500:
                self.right_paddle.move(up = False)


            output1 = winner_net.activate((self.ball.y, self.left_paddle.y, self.ball.x - self.left_paddle.x))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                self.genome1.fitness -= 0.01
            elif decision1 == 1:
                self.game.move_paddle(left=True, up = True)
            elif decision1 == 2:
                self.game.move_paddle(left=True, up = False)

        
            self.game.loop()
            self.game.draw()
            pygame.display.update()

    
    def train_ai(self,config, genome1, genome2,draw = True):
        net1 = neat.nn.FeedForwardNetwork.create(genome1,config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2,config)

        self.genome1 = genome1 
        self.genome2 = genome2

        max_hits = 50

        run = True 
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate((self.ball.y, self.left_paddle.y, self.ball.x - self.left_paddle.x))
            decision1 = output1.index(max(output1))

            if decision1 == 0:
                self.genome1.fitness -= 0.01
            elif decision1 == 1:
                self.game.move_paddle(left=True, up = True)
            elif decision1 == 2:
                self.game.move_paddle(left=True, up = False)


            output2 = net2.activate((self.ball.y, self.right_paddle.y, self.ball.x - self.right_paddle.x))
            decision2 = output2.index(max(output2))

            if decision2 == 0:
                self.genome2.fitness -= 0.01
            elif decision2 == 1:
                self.game.move_paddle(left=False, up = True)
            elif decision2 == 2:
                self.game.move_paddle(left=False, up = False)


            game_info = self.game.loop()

            

            if draw:
                self.game.draw(draw_hits=True, draw_score=False)
        
            pygame.display.update()

            if game_info.left_score == 1 or game_info.right_score == 1 or game_info.left_hits > max_hits:
                self.calculate_fitness(game_info)
                break


def eval_genomes(genomes, config):
    window_width, window_height = 700,500
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("neat pong")

    for i,(genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) -1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            pong = NEATGAME(window, window_width,window_height)
            pong.train_ai(config, genome1, genome2,draw = True)



def run_neat(config):
    #
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best_pong_nn", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):

    win_w, win_h = 700,500
    win = pygame.display.set_mode((win_w, win_h))
    pygame.display.set_caption("best pong net")

    with open("best_pong_nn", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = NEATGAME(win,win_w, win_h)
    game.test_ai(winner_net)


if __name__ == "__main__":
    config_path = '/Users/rnda/Desktop/CODING_PROJECTS/MY_NEAT_PONG_2/config.txt'

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    #run_neat(config)
    test_best_network(config)