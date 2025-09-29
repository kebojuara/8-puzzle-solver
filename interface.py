#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog

import main

algorithm = None
initialState = None
goalState = "123456780"
statepointer = cost = counter = depth = 0
runtime = 0.0
path = []

class InterfaceApp:

    def __init__(self, master=None):
        self._job = None
        self.appFrame = ttk.Frame(master)
        self.appFrame.configure(height=550, width=800)
        self.appFrame.pack(side="top")

        self.mainlabel = ttk.Label(self.appFrame)
        self.mainlabel.configure(
            anchor="center", font="{Arial} 36 {bold}", foreground="#000000", justify="center", text='8-Puzzle Solver')
        self.mainlabel.place(anchor="center", x=270, y=70)

        self.fastbackwardbutton = ttk.Button(self.appFrame, text='<<')
        self.fastbackwardbutton.configure(cursor="hand2")
        self.fastbackwardbutton.place(anchor="center", height=40, width=60, x=160, y=470)
        self.fastbackwardbutton.bind("<ButtonPress>", self.fastBackward)

        self.backbutton = ttk.Button(self.appFrame, text='Back')
        self.backbutton.configure(cursor="hand2")
        self.backbutton.place(anchor="center", height=40, width=60, x=230, y=470)
        self.backbutton.bind("<ButtonPress>", self.prevSequence)

        self.nextbutton = ttk.Button(self.appFrame, text='Next')
        self.nextbutton.configure(cursor="hand2")
        self.nextbutton.place(anchor="center", height=40, width=60, x=300, y=470)
        self.nextbutton.bind("<ButtonPress>", self.nextSequence)

        self.fastforwardbutton = ttk.Button(self.appFrame, text='>>')
        self.fastforwardbutton.configure(cursor="hand2")
        self.fastforwardbutton.place(anchor="center", height=40, width=60, x=370, y=470)
        self.fastforwardbutton.bind("<ButtonPress>", self.fastForward)

        self.stopbutton = ttk.Button(self.appFrame, text='STOP')
        self.stopbutton.configure(cursor="hand2", state='disabled')
        self.stopbutton.place(anchor="center", height=40, width=60, x=440, y=470)
        self.stopbutton.bind("<ButtonPress>", self.stopFastForward)

        self.resetbutton = ttk.Button(self.appFrame, text='Reset')
        self.resetbutton.configure(cursor="hand2", state='disabled')
        self.resetbutton.place(anchor="center", height=40, width=60, x=90, y=470)
        self.resetbutton.bind("<ButtonPress>", self.resetStepCounter)

        self.stepCount = ttk.Label(self.appFrame)
        self.stepCount.configure(anchor="center", background="#d6d6d6",
                                 font="{@Malgun Gothic Semilight} 12 {}", justify="center", text='Step: 0 / 0')
        self.stepCount.place(anchor="center", width=100, x=265, y=430)

        self.solvebutton = ttk.Button(self.appFrame)
        self.solvebutton.configure(cursor="hand2", text='Solve')
        self.solvebutton.place(anchor="center", height=50, width=150, x=700, y=70)
        self.solvebutton.bind("<ButtonPress>", self.solve)

        self.algorithmbox = ttk.Combobox(self.appFrame)
        self.algorithmbox.configure(cursor="hand2", state="readonly",
                                    values=('A* Manhattan', 'A* Euclidean', 'A* Tiles Out of Place',
                                            'GBFS Manhattan', 'GBFS Euclidean', 'GBFS Tiles Out of Place'))
        self.algorithmbox.place(anchor="center", height=30, width=150, x=700, y=150)
        self.algorithmbox.bind("<<ComboboxSelected>>", self.selectAlgorithm)

        self.algolabel = ttk.Label(self.appFrame)
        self.algolabel.configure(anchor="center", text='Search Algorithm:')
        self.algolabel.place(anchor="center", x=700, y=110)

        self.analysisbox = ttk.Label(self.appFrame)
        self.analysisbox.configure(anchor="center", text='', background="#d6d6d6", borderwidth=3, relief="sunken")
        self.analysisbox.place(anchor="center", width=150, height=240, x=700, y=370)

        self.heuristicsbox = ttk.Label(self.appFrame)
        self.heuristicsbox.configure(anchor="center", text='', background="#e6e6e6", borderwidth=3, relief="sunken")
        self.heuristicsbox.place(anchor="center", width=150, height=70, x=510, y=270)

        GRID_COLOR = "#cccccc"

        self.cell0 = ttk.Label(self.appFrame)
        self.cell0.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text=' ')
        self.cell0.place(anchor="center", height=100, width=100, x=170, y=170)
        self.cell1 = ttk.Label(self.appFrame)
        self.cell1.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='1')
        self.cell1.place(anchor="center", height=100, width=100, x=270, y=170)
        self.cell2 = ttk.Label(self.appFrame)
        self.cell2.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='2')
        self.cell2.place(anchor="center", height=100, width=100, x=370, y=170)
        self.cell3 = ttk.Label(self.appFrame)
        self.cell3.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='3')
        self.cell3.place(anchor="center", height=100, width=100, x=170, y=270)
        self.cell4 = ttk.Label(self.appFrame)
        self.cell4.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='4')
        self.cell4.place(anchor="center", height=100, width=100, x=270, y=270)
        self.cell5 = ttk.Label(self.appFrame)
        self.cell5.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='5')
        self.cell5.place(anchor="center", height=100, width=100, x=370, y=270)
        self.cell6 = ttk.Label(self.appFrame)
        self.cell6.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='6')
        self.cell6.place(anchor="center", height=100, width=100, x=170, y=370)
        self.cell7 = ttk.Label(self.appFrame)
        self.cell7.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='7')
        self.cell7.place(anchor="center", height=100, width=100, x=270, y=370)
        self.cell8 = ttk.Label(self.appFrame)
        self.cell8.configure(anchor="center", background=GRID_COLOR, borderwidth=3,
                             font="{Franklin Gothic Medium} 48 {}", justify="center", relief="sunken", text='8')
        self.cell8.place(anchor="center", height=100, width=100, x=370, y=370)

        self.enterstatebutton = ttk.Button(self.appFrame)
        self.enterstatebutton.configure(cursor="hand2", text='Enter initial state')
        self.enterstatebutton.place(anchor="center", width=150, x=700, y=190)
        self.enterstatebutton.bind("<ButtonPress>", self.enterInitialState)

        self.goalsatebutton = ttk.Button(self.appFrame)
        self.goalsatebutton.configure(cursor="hand2", text='Enter goal state')
        self.goalsatebutton.place(anchor="center", width=150, x=700, y=230)
        self.goalsatebutton.bind("<ButtonPress>", self.enterGoalState)

        self.mainwindow = self.appFrame

    def run(self):
        global goalState
        main.setGoalState(goalState)
        app.displayStateOnGrid('000000000')
        self.refreshFrame()
        self.mainwindow.mainloop()

    def prevSequence(self, event=None):
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer -= 1
            self.refreshFrame()

    def nextSequence(self, event=None):
        global statepointer
        if statepointer < len(path) - 1:
            self.stopFastForward()
            statepointer += 1
            self.refreshFrame()

    def solve(self, event=None):
        global algorithm, initialState
        if self.readyToSolve():
            self.resetGrid()
            self.solveState()
            if len(path) == 0:
                messagebox.showinfo('Unsolvable!', 'The state you entered is unsolvable')
                self.displaySearchAnalysis(True)
            else:
                self.refreshFrame()
        else:
            solvingerror = f'Cannot solve.\nAlgorithm in use: {algorithm}\nInitial State: {initialState}'
            messagebox.showerror('Cannot Solve', solvingerror)

    def enterInitialState(self, event=None):
        global initialState, statepointer
        inputState = simpledialog.askstring('Initial State Entry', 'Enter your initial state (9 digits, 0 for blank):')
        if inputState and self.validateState(inputState):
            initialState = inputState
            self.reset()
            app.displayStateOnGrid(initialState)
        else:
            messagebox.showerror('Input Error', 'Invalid initial state')

    def enterGoalState(self, event=None):
        global goalState
        inputState = simpledialog.askstring('Goal State Entry', 'Enter your goal state (9 digits, 0 for blank):')
        if inputState and self.validateState(inputState):
            goalState = inputState
            main.setGoalState(goalState)
            self.reset()
        else:
            messagebox.showerror('Input Error', 'Invalid goal state')

    def selectAlgorithm(self, event=None):
        global algorithm
        try:
            choice = self.algorithmbox.selection_get()
            self.reset()
            algorithm = choice
        except:
            pass

    def fastForward(self, event=None):
        global statepointer
        self.stopFastForward()
        if statepointer < cost:
            app.stopbutton.configure(state='enabled')
            statepointer += 1
            self.refreshFrame()
            ms = 100
            if 100 < cost <= 1000:
                ms = 20
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastForward)
        else:
            self.stopFastForward()

    def fastBackward(self, event=None):
        global statepointer
        self.stopFastForward()
        if statepointer > 0:
            app.stopbutton.configure(state='enabled')
            statepointer -= 1
            ms = 50
            if cost > 1000:
                ms = 1
            app._job = app.stepCount.after(ms, self.fastBackward)
        else:
            self.stopFastForward()
        self.refreshFrame()

    @staticmethod
    def stopFastForward(event=None):
        if app._job is not None:
            app.stopbutton.configure(state='disabled')
            app.stepCount.after_cancel(app._job)
            app._job = None

    def resetStepCounter(self, event=None):
        global statepointer
        if statepointer > 0:
            self.stopFastForward()
            statepointer = 0
            self.refreshFrame()

    def displayHeuristics(self, state):
        global algorithm, statepointer
        if algorithm is None or cost == 0:
            app.heuristicsbox.configure(text='')
            return

        g = statepointer
        h = 0
        if 'Manhattan' in algorithm:
            h = main.getManhattanDistance(state)
        elif 'Euclidean' in algorithm:
            h = main.getEuclideanDistance(state)
        elif 'Tiles Out of Place' in algorithm:
            h = main.getTilesOutOfPlace(state)

        h_display = int(round(h))

        if algorithm.startswith("A*"):
            f = g + h_display
            text = f"g(n) = {g}\nh(n) = {h_display}\nf(n) = {f}"
        else:
            text = f"h(n) = {h_display}"

        app.heuristicsbox.configure(text=text)

    def displaySearchAnalysis(self, force_display=False):
        if self.solved() or force_display is True:
            analytics = f'Analysis of\n{algorithm}\n\nInitial state : {initialState}\nGoal state : {main.goal_state}'
            if force_display:
                analytics += '\n< UNSOLVABLE >'
            analytics += '\n-------------------------------\n' \
                         f'Nodes expanded:\n{counter}\n' \
                         f'Search depth:\n{depth}\n' \
                         f'Search cost:\n{cost}\n' \
                         f'Running Time:\n{runtime:.6f} s'
        else:
            analytics = ''
        app.analysisbox.configure(text=analytics)

    def displayStateOnGrid(self, state):
        if not self.validateState(state):
            state = '000000000'
        self.cell0.configure(text=self.adjustDigit(state[0]))
        self.cell1.configure(text=self.adjustDigit(state[1]))
        self.cell2.configure(text=self.adjustDigit(state[2]))
        self.cell3.configure(text=self.adjustDigit(state[3]))
        self.cell4.configure(text=self.adjustDigit(state[4]))
        self.cell5.configure(text=self.adjustDigit(state[5]))
        self.cell6.configure(text=self.adjustDigit(state[6]))
        self.cell7.configure(text=self.adjustDigit(state[7]))
        self.cell8.configure(text=self.adjustDigit(state[8]))

    @staticmethod
    def readyToSolve():
        return initialState is not None and algorithm is not None

    @staticmethod
    def solved():
        return len(path) > 0

    @staticmethod
    def solveState():
        global path, cost, counter, depth, runtime

        if str(algorithm) == 'A* Manhattan':
            main.AStarSearch_manhattan(initialState)
            path, cost, counter, depth, runtime = \
                main.manhattan_path, main.manhattan_cost, main.manhattan_counter, main.manhattan_depth, main.time_manhattan
        elif str(algorithm) == 'A* Euclidean':
            main.AStarSearch_euclid(initialState)
            path, cost, counter, depth, runtime = \
                main.euclid_path, main.euclid_cost, main.euclid_counter, round(main.euclid_depth), main.time_euclid
        elif str(algorithm) == 'A* Tiles Out of Place':
            main.AStarSearch_tiles_out_of_place(initialState)
            path, cost, counter, depth, runtime = \
                main.tiles_out_of_place_path, main.tiles_out_of_place_cost, main.tiles_out_of_place_counter, main.tiles_out_of_place_depth, main.time_tiles_out_of_place
        elif str(algorithm) == 'GBFS Manhattan':
            main.GreedyBestFirstSearch_manhattan(initialState)
            path, cost, counter, depth, runtime = \
                main.gbfs_manhattan_path, main.gbfs_manhattan_cost, main.gbfs_manhattan_counter, main.gbfs_manhattan_depth, main.time_gbfs_manhattan
        elif str(algorithm) == 'GBFS Euclidean':
            main.GreedyBestFirstSearch_euclid(initialState)
            path, cost, counter, depth, runtime = \
                main.gbfs_euclid_path, main.gbfs_euclid_cost, main.gbfs_euclid_counter, main.gbfs_euclid_depth, main.time_gbfs_euclid
        elif str(algorithm) == 'GBFS Tiles Out of Place':
            main.GreedyBestFirstSearch_tiles_out_of_place(initialState)
            path, cost, counter, depth, runtime = \
                main.gbfs_tiles_out_of_place_path, main.gbfs_tiles_out_of_place_cost, main.gbfs_tiles_out_of_place_counter, main.gbfs_tiles_out_of_place_depth, main.time_gbfs_tiles_out_of_place


    def resetGrid(self):
        global statepointer
        statepointer = 0
        self.refreshFrame()
        app.stepCount.configure(text=self.getStepCountString())

    def reset(self):
        global path, cost, counter, runtime
        cost = counter = 0
        runtime = 0.0
        path = []
        self.resetGrid()
        app.analysisbox.configure(text='')
        app.heuristicsbox.configure(text='')

    @staticmethod
    def getStepCountString():
        return f'Step: {statepointer} / {cost}'

    @staticmethod
    def refreshFrame():
        if cost > 0:
            state = main.getStringRepresentation(path[statepointer])
            app.displayStateOnGrid(state)
            app.stepCount.configure(text=app.getStepCountString())
            app.displaySearchAnalysis()
            app.displayHeuristics(state)

        if statepointer == 0:
            app.resetbutton.configure(state='disabled')
            app.backbutton.configure(state='disabled')
            app.fastbackwardbutton.configure(state='disabled')
        else:
            app.resetbutton.configure(state='enabled')
            app.backbutton.configure(state='enabled')
            app.fastbackwardbutton.configure(state='enabled')

        if cost == 0 or statepointer == cost:
            app.fastforwardbutton.configure(state='disabled')
            app.nextbutton.configure(state='disabled')
        else:
            app.fastforwardbutton.configure(state='enabled')
            app.nextbutton.configure(state='enabled')

    @staticmethod
    def validateState(inputState):
        seen = []
        if inputState is None or len(inputState) != 9 or not inputState.isnumeric():
            return False
        for dig in inputState:
            if dig in seen or dig == '9':
                return False
            seen.append(dig)
        return True

    @staticmethod
    def adjustDigit(dig):
        if dig == '0':
            return ' '
        return dig


if __name__ == "__main__":
    global app
    root = tk.Tk()
    root.title('8-Puzzle Solver')
    app = InterfaceApp(root)
    app.run()