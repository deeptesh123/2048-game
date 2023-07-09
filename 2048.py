import tkinter as tk
import tkinter.messagebox as msg
import appearance as ap
import random
import copy
class Grid:
    def __init__(self,board_size):
        self.size=board_size
        self.grid=self.create_empty_grid()
        self.moved=False
        self.curr_score=0
    def create_empty_grid(self):
        return [[0]*self.size for i in range(self.size)]
    def retrieve_empty_cells(self):
        empty=[]
        for row in range(self.size):
            for col in range(self.size):
                if(self.grid[row][col]==0):
                    empty.append([row,col])
        return empty
    def select_random_cell(self):
        cell=random.choice(self.retrieve_empty_cells())
        row,col=cell[0],cell[1]
        if(random.random()<0.9):
            self.grid[row][col]=2
        else:
            self.grid[row][col]=4
    def reverse_row(self,row):
        rev_row=[]
        for i in range(self.size-1,-1,-1):
            rev_row.append(row[i])
        return rev_row
    def reverse_grid(self):
        r_grid=[]
        for i in range(self.size):
            r_grid.append(self.reverse_row(self.grid[i]))
        self.grid=r_grid
    def transpose(self):
        t=self.create_empty_grid()
        for row in range(self.size):
            for col in range(self.size):
                t[row][col]=self.grid[col][row]
        self.grid=t
    def row_merge_left(self,row):
        for i in range(self.size-1):
            for j in range(self.size-1,0,-1):
                if row[j-1]==0 and row[j]!=0:
                    row[j-1]=row[j]
                    row[j]=0
        for i in range(self.size-1):
            if row[i]==row[i+1]:
                row[i]*=2
                self.curr_score+=row[i]
                row[i+1]=0
        for i in range(self.size-1,0,-1):
            if row[i-1]==0 and row[i]!=0:
                row[i-1]=row[i]
                row[i]=0
        return row
    def grid_merge_left(self):
        initial=copy.deepcopy(self.grid)
        for i in range(self.size):
            self.grid[i]=self.row_merge_left(self.grid[i])
        if self.grid!=initial:
            self.moved=True
    def can_merge(self):
        for row in range(self.size):
            for col in range(self.size-1):
                if self.grid[row][col]==self.grid[row][col+1]:
                    return True
        for row in range(self.size-1):
            for col in range(self.size):
                if self.grid[row][col]==self.grid[row+1][col]:
                    return True      
        return False
    def has_empty_cells(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col]==0:
                    return True
        return False
    def reached_2048(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col]==2048:
                    return True
        return False
class GUI:
    def __init__(self,grid):
        self.grid=grid
        self.root=tk.Tk()
        self.root.title("2048")
        self.game_panel=tk.Frame(self.root,bg=ap.BACKGROUND_COLOR)
        self.upper_panel=tk.Frame(self.root,bg="white",)
        self.cell_labels=[]
        for row in range(self.grid.size):
            row_cell_labels=[]
            for col in range(self.grid.size):
                label=tk.Label(self.game_panel,text="",bg=ap.EMPTY_CELL_COLOR,font=ap.FONT,justify=tk.CENTER,width=4,height=2)
                label.grid(row=row,column=col,padx=10,pady=10)
                row_cell_labels.append(label)
            self.cell_labels.append(row_cell_labels)
        self.game_panel.grid(row=1,column=0)
        self.upper_panel.grid(row=0,column=0)
    def start_upper_panel(self):
        l1=tk.Label(self.upper_panel,text=f"SCORE\n{self.grid.curr_score}",font=ap.FONT,bg=ap.BACKGROUND_COLOR,fg="white",height=3,width=6)
        l2=tk.Label(self.upper_panel,text="2048",font=ap.TITLE_FONT,bg="#FFDB58",fg="white",height=3,width=5)
        l3=tk.Label(self.upper_panel,text="BEST\n0",font=ap.FONT,bg=ap.BACKGROUND_COLOR,fg="white",height=3,width=6)
        l1.grid(row=0,column=0,pady=10,padx=10)
        l2.grid(row=0,column=1,pady=10,padx=10)
        l3.grid(row=0,column=2,pady=10,padx=10)
    def start(self):
        self.start_upper_panel()
        for row in range(self.grid.size):
            for col in range(self.grid.size):
                cell_text=str(self.grid.grid[row][col])
                if self.grid.grid[row][col]==0:
                    self.cell_labels[row][col].configure(text="",bg=ap.EMPTY_CELL_COLOR)
                else:
                    if(self.grid.grid[row][col]>=2048):
                        bg_color=ap.CELL_BACKGROUND_COLOR_DICT['beyond']
                        fg_color=ap.CELL_COLOR_DICT['beyond']
                    else:
                        bg_color=ap.CELL_BACKGROUND_COLOR_DICT[cell_text]
                        fg_color=ap.CELL_COLOR_DICT[cell_text]
                    self.cell_labels[row][col].configure(text=cell_text,bg=bg_color,fg=fg_color)
class Game_flow:
    def __init__(self,grid,gui):
        self.won=False
        self.over=False
        self.want_to_continue=False
        self.grid=grid
        self.gui=gui
        self.undo_1=self.grid.create_empty_grid()
        self.undo_2=self.grid.create_empty_grid()
        self.prev_score_1=0
        self.prev_score_2=0
        self.undone=False
    def game_over(self):
        return self.over or (self.won and not self.want_to_continue)
    def set_random_cells(self):
        for i in range(2):
            self.grid.select_random_cell()
    def initialize(self):
        self.set_random_cells()
        self.gui.start()
        self.gui.root.bind('<Key>',self.movements)
        self.gui.root.mainloop()
    def can_move(self):
        return self.grid.can_merge() or self.grid.has_empty_cells()
    def merge_left(self):
        self.grid.grid_merge_left()
    def merge_right(self):
        self.grid.reverse_grid()
        self.grid.grid_merge_left()
        self.grid.reverse_grid()
    def merge_up(self):
        self.grid.transpose()
        self.grid.grid_merge_left()
        self.grid.transpose()
    def merge_down(self):
        self.grid.transpose()
        self.grid.reverse_grid()
        self.grid.grid_merge_left()
        self.grid.reverse_grid()
        self.grid.transpose()
    def undo(self):
        self.grid.grid=self.undo_2
        self.grid.curr_score=self.prev_score_2
        self.grid.moved=True
        self.undone=True
    def print_grid(self,gg):
        for i in range(self.grid.size):
            for j in range(self.grid.size):
                print(gg[i][j],end=" |")
            print()
    def movements(self,event):
        if self.game_over(): return
        self.grid.moved=False
        self.undone=False
        key_value=event.keysym
        self.undo_1=copy.deepcopy(self.grid.grid)
        self.prev_score_1=self.grid.curr_score
        if(key_value in ap.LEFT_KEYS): self.merge_left()
        if(key_value in ap.RIGHT_KEYS): self.merge_right()
        if(key_value in ap.UP_KEYS): self.merge_up()
        if(key_value in ap.DOWN_KEYS): self.merge_down()
        if(key_value in ["z","Z"]): self.undo()
        self.undo_2=copy.deepcopy(self.undo_1)
        self.prev_score_2=self.prev_score_1
        if self.grid.moved:
            if not self.undone: self.grid.select_random_cell()
            self.gui.start()
            if(self.grid.reached_2048()):
                if(self.won==True): return
                self.won=True
                ans=msg.askyesno("You Won","Do you want to continue the game?")
                if ans=="yes": self.want_to_continue=True
                self.game_over()
            if(self.can_move()==False):
                msg.showinfo("Game over","Chal bsdk, game teri aukaat se bahar jaa chuki hai!")
                self.over=True
                self.game_over()
        
size=4
grid=Grid(size)
gui=GUI(grid)
game=Game_flow(grid,gui)
game.initialize()


                




            
            
