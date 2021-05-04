import itertools
import random

import numpy as np

PAYOUTS = (10_000, 36, 720, 360, 80,
           252, 108, 72, 54, 180,
           72, 180, 119, 36, 306,
           1_080, 144, 1_800, 3_600
           )

def show_payout():
    toppp = " _____________________________________________________________________ "
    dlu_0 = "|             |             |             |             |             |"
    row_0 = "|  6 => 10000 |   7 => 36   |   8 => 720  |   9 => 360  |  10 => 80   |"
    dlm_0 = "|_____________|_____________|_____________|_____________|_____________|"
    dlu_1 = "|             |             |             |             |             |"
    row_1 = "| 11 => 252   |  12 => 108  |  13 => 72   |  14 => 54   |  15 => 180  |"
    dlm_1 = "|_____________|_____________|_____________|_____________|_____________|"
    dlu_2 = "|             |             |             |             |             |"
    row_2 = "| 16 => 72    |  17 => 180  |  18 => 119  |  19 => 36   |  20 => 306  |"
    dlm_2 = "|_____________|_____________|_____________|_____________|_____________|"
    dlu_b = "|             |             |             |             |"
    row_b = "| 21 => 1080  |  22 => 144  |  23 => 1800 |  24 => 3600 |"
    bottm = "|_____________|_____________|_____________|_____________|"
    print(f"{toppp}\n{dlu_0}\n{row_0}\n{dlm_0}")
    print(f"{dlu_1}\n{row_1}\n{dlm_1}")
    print(f"{dlu_2}\n{row_2}\n{dlm_2}")
    print(f"{dlu_b}\n{row_b}\n{bottm}")

class Ticket:
    def __init__(self):
        self.__ticket = np.zeros((3, 3), dtype=int)
        self.__covers = np.array([['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']])

    @property
    def ticket(self):
        return self.__ticket

    @property
    def covers(self):
        return self.__covers

    def set_slot(self, y, x, val):
        assert 0 <= y <= 2, "Must input a valid row index"
        assert 0 <= x <= 2, "Must input a valid column index"
        assert 1 <= val <= 9, "Value being added must be between 1 and 9"
        assert not val in self.__ticket.flatten(), "Cannot set a value that is already on the ticket"
        assert self.ticket[y][x] == 0, "Cannot set a slot where it is already set"

        self.ticket[y][x] = val

    def can_uncover_slot(self, y, x):
        return self.__covers[y][x] == 'O'

    def uncover_slot(self, y, x):
        assert 0 <= y <= 2, "Must input a valid row index"
        assert 0 <= x <= 2, "Must input a valid column index"

        if not self.can_uncover_slot(y, x):
            return

        self.__covers[y][x] = self.ticket[y][x]

    def uncover_all(self):
        for i in range(3):
            for j in range(3):
                self.uncover_slot(y=i, x=j)

    def sum_group(self, selector, index=None):
        assert selector in ['r', 'c', 'd', 'a']
        assert selector in ['r', 'c'] and not index is None and index in range(3) if not selector in ['d',
                                                                                                      'a'] else True
        assert selector in ['d', 'a'] if not selector in ['r', 'c'] else True

        if selector == 'a':
            return self.ticket[0][2] + self.ticket[1][1] + self.ticket[2][0]
        elif selector == 'd':
            return self.ticket[0][0] + self.ticket[1][1] + self.ticket[2][2]
        elif selector == 'c':
            return self.ticket[0][index] + self.ticket[1][index] + self.ticket[2][index]
        else:
            return self.ticket[index][0] + self.ticket[index][1] + self.ticket[index][2]

    def show_ticket(self):
        ticket_str = " _______ _______ _______\n"
        topp_delim = "|       |       |       |"
        botm_delim = "|_______|_______|_______|"
        for i, row in enumerate(self.ticket):
            ticket_str += topp_delim + '\n'
            for j, col in enumerate(row):
                ticket_str += f"|   {str(col)}   "
            ticket_str = ticket_str + "|\n" + botm_delim + '\n'

        print(ticket_str.rstrip())

    def __str__(self):
        ticket_str = " _______ _______ _______\n"
        topp_delim = "|       |       |       |"
        botm_delim = "|_______|_______|_______|"
        for i, row in enumerate(self.covers):
            ticket_str += topp_delim + '\n'
            for j, col in enumerate(row):
                ticket_str += f"|   {str(col)}   "
            ticket_str = ticket_str + "|\n" + botm_delim + '\n'

        return ticket_str.rstrip()

class RandomTicket(Ticket):
    def __init__(self):
        super().__init__()
        valid_coor = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), ]
        valid_val = list(range(1, 10))
        for _ in range(9):
            coor_index = 0 if len(valid_coor) == 0 else random.randint(0, len(valid_coor) - 1)
            val = 0 if len(valid_val) == 0 else random.randint(0, len(valid_val) - 1)
            coor = valid_coor.pop(coor_index)

            self.set_slot(y=coor[0], x=coor[1], val=valid_val.pop(val))

    def __str__(self):
        return super().__str__()

ROW_0, ROW_1, ROW_2, COL_0, COL_1, COL_2, DIAG, ANTI, = range(8)

class MiniCactBot:
    def __init__(self, ticket):
        self.__ticket = ticket
        self.__scratches = 0

    @property
    def ticket(self):
        return self.__ticket

    @property
    def scratches(self):
        return self.__scratches

    @staticmethod
    def get_payout(group_sum):
        assert 6 <= group_sum <= 24
        return PAYOUTS[group_sum - 6]

    def __finish(self, group):
        group_sum = self.ticket.sum_group(*group)
        self.ticket.uncover_all()
        print(self.ticket)
        print(f"Using grouping: {group}")
        print(f"Payout: {self.get_payout(group_sum)}")

class MiniCactBotGame(MiniCactBot):
    def __init__(self, ticket):
        super().__init__(ticket)
        self.__ticket.uncover_slot(y=random.randint(0, 2), x=random.randint(0, 2))

    def __select_slots_to_uncover(self):
        valid_slot = False
        attempts = 1
        while not valid_slot:
            print(f"Scratches left: {3 - self.scratches}")
            if attempts % 5 == 1:
                print("Pick a slot to uncover. Type as 'y,x' coordinates.")
                print("Note: The top left is '0,0'")
                print(self.ticket)
            try:
                print(">>>", end=' ')
                slot_str = input().strip()
                aux = slot_str.split(',')
                if len(aux) != 2:
                    print("You've put either extra or no commas in your input. Please try again.")
                    attempts += 1
                    continue
                y, x = int(aux[0].strip()), int(aux[1].strip())
                if not 0 <= y <= 2:
                    print("You've input an invalid row. Please try again.")
                    attempts += 1
                    continue
                if not 0 <= x <= 2:
                    print("You've input an invalid column. Please try again.")
                    attempts += 1
                    continue
                if not self.ticket.can_uncover_slot(y=y, x=x):
                    print("You've already uncovered that slot. Please try another.")
                    attempts += 1
                    continue
                return y, x
            except ValueError as _:
                print("The coordinates you tried to input are not integers. Please try again.")

    def __select_group_for_payout(self):
        valid_selection = False
        attempts = 1
        while not valid_selection:
            if attempts % 5 == 1:
                show_payout()
                print("Your Ticket:")
                print(self.ticket)
                print("Select a grouping you want to cash out on.")
                print("Example input:")
                print("'r 0' is the row labelled 0")
                print("'c 2' is the column labelled 2")
                print("'d' is the diagonal from left to right")
                print("'a' is the diagonal from right to left")
            try:
                print(">>>", end=' ')
                group = input().lower().strip()
                group_split = group.split(' ')

                if len(group_split) > 2:
                    print("You've put either extra or no spaces in between your selectors. Please try again.")
                    attempts += 1
                    continue
                if not group_split[0] in ['r', 'c', 'd', 'a']:
                    print("Your first selector is not a valid one. Please try again")
                    attempts += 1
                    continue
                if len(group_split) == 2:
                    index = int(group_split[1])
                    if not index in range(3):
                        print("Your second selector must be between 0 and 2. Please try again")
                        attempts += 1
                        continue
                    else:
                        group_split[1] = index

                return group_split

            except ValueError as _:
                print("You tried to input that are not integers for selecting a row or column. Please try again.")

    def __make_scratches(self):
        while self.scratches < 3:
            y, x = self.__select_slots_to_uncover()
            self.ticket.uncover_slot(y=y, x=x)
            self.__scratches += 1

    def play(self):
        self.__make_scratches()
        group = self.__select_group_for_payout()
        self.__finish(group)

class MiniCactBotSolver:
    def __init__(self, ticket):
        self.__ticket = ticket
        self.__ticket.show_ticket()

    def get_uncovered_numbers(self):
        return tuple(val for val in range(1, 10) if not val in self.__ticket.ticket.flatten())

    def get_combinations(self):
        """
        go through each row dia and col, calculate potential points given the end state.
        # [row0, row1, row2, col0, col1, col2, dia, ant]
        """

        # print(self.ticket)
        uncovered_numbers = self.get_uncovered_numbers()
        # print(uncovered_numbers)

        current_state = ((self.__ticket.ticket[0][0], self.__ticket.ticket[0][1], self.__ticket.ticket[0][2]),
                         (self.__ticket.ticket[1][0], self.__ticket.ticket[1][1], self.__ticket.ticket[1][2]),
                         (self.__ticket.ticket[2][0], self.__ticket.ticket[2][1], self.__ticket.ticket[2][2]),
                         (self.__ticket.ticket[0][0], self.__ticket.ticket[1][0], self.__ticket.ticket[2][0]),
                         (self.__ticket.ticket[0][1], self.__ticket.ticket[1][1], self.__ticket.ticket[2][1]),
                         (self.__ticket.ticket[0][2], self.__ticket.ticket[1][2], self.__ticket.ticket[2][2]),
                         (self.__ticket.ticket[0][0], self.__ticket.ticket[1][1], self.__ticket.ticket[2][2]),
                         (self.__ticket.ticket[0][2], self.__ticket.ticket[1][1], self.__ticket.ticket[2][0]),)

        groups = []
        for group in current_state:
            aux = []
            aux.extend(uncovered_numbers)
            group = [int(val) for val in group if val != 0]
            aux.extend(group)
            groups.append(aux)

        all_combinations = []

        for where, group in enumerate(groups):
            must_have_me = group[len(uncovered_numbers):]

            if len(must_have_me) == 3:
                combinations = [tuple(must_have_me)]
            else:
                combinations = list(itertools.combinations(group, 3))

            if must_have_me:
                combinations = [combination for combination in combinations if all(val in combination for val in
                                                                                   must_have_me)]
            combinations = [combination for combination in combinations if 6 <= sum(combination) <= 24]

            all_combinations.append(combinations)

        return [combinations for combinations in all_combinations if len(combinations) <= 5]

    def solve(self):
        all_combinations = self.get_combinations()
        solver = self.__group_averaging
        group = solver(all_combinations)
        print(group)

    def __high_roll(self, all_combinations):
        best_cases = []
        for group in all_combinations:
            group_sums = tuple(sum(combination) for combination in group)
            # best_sum = -1
            # best_prob = -1
            # max_payout = -1
            # for sum_ in set(sums):
            #     payout = PAYOUTS[sum_-6]
            #     prob = sums.count(sum_) / len(sums)
            #     # print(f"Probability of getting a sum of {sum_:2} is {prob:.4f}")
            #     if max_payout < payout:
            #         max_payout = payout
            #         best_sum = sum_
            #         best_prob = prob
        print(best_cases)

        assert len(best_cases) == 8, "Something went wrong"

    def __best_ev(self):
        ...

    def __group_averaging(self, all_combinations):
        print("Solving by using the best average of all groupings")
        avg_cases = []
        for group in all_combinations:
            group_sums = tuple(sum(combination) for combination in group)
            group_sum = sum(group_sums)
            group_avg = group_sum / len(group_sums)
            avg_cases.append(group_avg)

        # print(avg_cases)

        assert len(avg_cases) == len(all_combinations), "Something went wrong"

        best_avg = max(avg_cases)
        where = avg_cases.index(best_avg)
        group = self.__get_selectors_from_flat(where)

        return group

    def __get_selectors_from_flat(self, where):
        group = []
        if 0 <= where <= 2:
            group.append('r')
            group.append(where)
        elif 3 <= where <= 5:
            group.append('c')
            group.append(where)
        elif where == 6:
            group.append('d')
        else:
            group.append('a')
        return group

    # def __pure_probability(self, all_combinations):
    #     remember_segments = [len(combinations) for combinations in all_combinations]
    #     flat_all_combinations_sums = tuple(sum(group) for combinations in all_combinations for group in combinations)
    #     print(remember_segments)
    #     print(flat_all_combinations_sums)
    #     for sum_ in set(flat_all_combinations_sums):
    #         prob = flat_all_combinations_sums.count(sum_) / len(flat_all_combinations_sums)
    #         print(f"Probability of getting a sum of {sum_} is {prob:.4f}")

def str_with_row_col_dia(self):
    ticket_str = f"D 0 1 2 A\n"
    for i, row in enumerate(self.ticket.covers):
        new_row = f"{i} "
        for j, col in enumerate(row):
            new_row += str(col) + ' '

        new_row = new_row.strip() + '\n'
        ticket_str += new_row

    return ticket_str.strip()

def __str__(self):
    return f"Scratches left: {3 - self.scratches}\n{self.ticket}"

def main():
    ticket = Ticket()
    ticket.set_slot(0, 0, 1)
    ticket.set_slot(1, 1, 2)
    ticket.set_slot(2, 2, 3)
    ticket.set_slot(1, 0, 5)
    solver = MiniCactBotSolver(ticket)
    solver.solve()

if __name__ == "__main__":
    main()
