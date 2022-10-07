import logic


def main():
    mat = logic.start_game()

    while (True):
        x = input("Press the command : ")

        if (x == 'W' or x == 'w'):
            mat, mat_changed = logic.move_up(mat)
        elif (x == 'S' or x == 's'):
            mat, mat_changed = logic.move_down(mat)
        elif (x == 'A' or x == 'a'):
            mat, mat_changed = logic.move_left(mat)
        elif (x == 'D' or x == 'd'):
            mat, mat_changed = logic.move_right(mat)
        else:
            print("Invalid Key Pressed")
            continue

        game_finished = logic.is_game_finished(mat)

        if game_finished == 0 and mat_changed is False:
            print("Invalid Move")
            continue

        if (game_finished == 0):
            logic.add_new_2(mat)
        else:
            print("GAME OVER")
            break

        logic.print_mat(mat)


if __name__ == '__main__':
    main()
