import logic


def main():
    mat = logic.start_game()

    while (True):

        x = input("Press the command : ")

        if (x == 'W' or x == 'w'):
            mat, flag = logic.move_up(mat)
        elif (x == 'S' or x == 's'):
            mat, flag = logic.move_down(mat)
        elif (x == 'A' or x == 'a'):
            mat, flag = logic.move_left(mat)
        elif (x == 'D' or x == 'd'):
            mat, flag = logic.move_right(mat)
        else:
            print("Invalid Key Pressed")
            continue

        status = logic.is_game_finished(mat)
        print("GAME IS NOT OVER" if status == 0 else "GAME OVER")

        if (status == 0):
            logic.add_new_2(mat)
        else:
            break

        # print the matrix after each move.
        logic.print_mat(mat)


if __name__ == '__main__':
    main()
