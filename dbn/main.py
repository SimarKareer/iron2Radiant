from dbn.Game import Game

def main():
    game = Game(100)

    obs = [
        [("Raze", 50, 50)], [("Brimstone", 40, 70)], [("Brimstone", 10, 50)]
    ]

    count = 0
    while True:
        Game.tick(obs[count])
        count += 1

main()