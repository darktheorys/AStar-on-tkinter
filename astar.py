from tkinter import Canvas, Frame, BOTH
from tkinter import messagebox

import random
import tkinter as tk
import math


HEIGHT, WIDTH = 720, 1368
ROW, COLUMN = 16, 32
OFFSET = 8

class Node():
    def __init__(self, i, j, canvas):
        w_size = WIDTH // COLUMN
        h_size = HEIGHT // ROW

        x, y = j * w_size + OFFSET, i*h_size + OFFSET
        x2 = x + w_size - OFFSET
        y2 = y + h_size - OFFSET

        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x2, y2,
                    outline="black", fill="gray", width=2)
        
        self.i, self.j = i, j
        self.isObstacle = False
        self.isVisited = False
        self.parent = None
        self.localGoal = float("inf")
        self.globalGoal = float("inf")
        self.idx = COLUMN * i + j + 1
        self.lineid = None
        
        self.neighbors = []
        if i > 0:
            self.neighbors.append((i-1, j))
        if i < (ROW-1):
            self.neighbors.append((i+1, j))
        if j > 0:
            self.neighbors.append((i, j-1))
        if j < (COLUMN-1):
            self.neighbors.append((i, j+1))
        if i > 0 and j > 0:
            self.neighbors.append((i-1, j-1))
        if i < (ROW-1) and j < (COLUMN-1):
            self.neighbors.append((i+1, j+1))
        if i > 0 and j < (COLUMN-1):
            self.neighbors.append((i-1, j+1))
        if i < (ROW-1) and j > 0:
            self.neighbors.append((i+1, j-1))
          
    def click(self):
        if self.canvas.itemcget(self.idx, "fill") not in ["red", "green"]:
            self.isObstacle = not self.isObstacle
            self.canvas.itemconfig(self.idx, fill="blue" if self.isObstacle else "gray")
    
    def visit(self):
        self.canvas.itemconfig(self.idx, fill="skyblue")
            
    def unvisit(self):
        if self.isVisited and self.canvas.itemcget(self.idx, "fill") not in ["red", "green"] :
            self.canvas.itemconfig(self.idx, fill="blue" if  self.isObstacle else "gray")
            
    
    def reset(self, isTargStart=False):
        if isTargStart:
            if self.isObstacle:
                self.canvas.itemconfig(self.idx, fill="blue")
            else:
                self.canvas.itemconfig(self.idx, fill="gray")

        if self.lineid is not None:
            self.canvas.delete(self.lineid)
    
    def click2(self):
        self.isObstacle = False
        if self.canvas.itemcget(self.idx, "fill") != "green":
            self.canvas.itemconfig(self.idx, fill="green")
        else:
            self.canvas.itemconfig(self.idx, fill="gray")
    
    def click3(self):
        self.isObstacle = False
        if self.canvas.itemcget(self.idx, "fill") != "red":
            self.canvas.itemconfig(self.idx, fill="red")
        else:
            self.canvas.itemconfig(self.idx, fill="gray")
            
    def click4(self, prev):
        w_size = WIDTH // COLUMN
        h_size = HEIGHT // ROW

        x, y = self.j * w_size + OFFSET, self.i*h_size + OFFSET
        x2 = x + w_size - OFFSET
        y2 = y + h_size - OFFSET
        x, y = (x+x2)/2, (y+y2)/2
        

        xx, yy = prev.j * w_size + OFFSET, prev.i*h_size + OFFSET
        xx2 = xx + w_size - OFFSET
        yy2 = yy + h_size - OFFSET
        xx, yy = (xx+xx2)/2, (yy+yy2)/2
        
        self.lineid = self.canvas.create_line(x, y, xx, yy, width=5, fill="black")
        self.canvas.lower(self.lineid)
        

        
class UI(Frame):

    def __init__(self, stopWhenFind):
        super().__init__()
        self.stopWhenFind = stopWhenFind
        self.initUI()


    def initUI(self):

        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.path = []
        self.nodes = []
        self.canvas = Canvas(self)
        for i in range(ROW):
            for j in range(COLUMN):
                self.nodes.append(Node(i, j, self.canvas))

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-2>", self.click2)
        self.canvas.bind("<Button-3>", self.click3)
        self.canvas.pack(fill=BOTH, expand=1)
        self.target = random.randint(1, len(self.nodes)) - 1
        self.start =  random.randint(1, len(self.nodes)) - 1
        while self.start == self.target:
            self.start = random.randint(1, len(self.nodes)) - 1
        self.nodes[self.start].click2()
        self.nodes[self.target].click3()
        
        self.solve()
        
        

    def click(self, event):
        try:
            canvas_item_id = event.widget.find_withtag('current')[0]
            self.nodes[canvas_item_id-1].click()
        except:
            pass
        
        self.solve()
       
       
    def click2(self, event):
        try:
            canvas_item_id = event.widget.find_withtag('current')[0]
            if self.nodes[self.start] is not None:
                self.nodes[self.start].reset(True)
            self.start = canvas_item_id-1
            self.nodes[self.start].click2()
        except:
            pass
            
        self.solve()
         
    def click3(self, event):
        try:
            canvas_item_id = event.widget.find_withtag('current')[0]
            if self.target is not None:
                self.nodes[self.target].reset(True)
            self.target = canvas_item_id-1
            self.nodes[self.target].click3()
        except:
            pass
        
        self.solve()
    
    def solve(self):
        for node in self.path:
            self.nodes[node].reset()
            
        for node in self.nodes:
            node.localGoal = float("inf")
            node.globalGoal = float("inf")
            node.parent = None
            if node not in [self.start, self.target]:
                node.unvisit()
            node.isVisited = False
            
             
        self.path = []
        distance = lambda node1, node2:  math.sqrt((node1.i - node2.i)**2 + (node1.j-node2.j)**2)

        self.nodes[self.start].localGoal = 0.0
        self.nodes[self.start].globalGoal = distance(self.nodes[self.start], self.nodes[self.target])
         
        node_list = [self.start]
        node_size = 1
        
        while node_size > 0:
            node_list.sort(key= lambda k: self.nodes[k].globalGoal)
            
            while node_size > 0:
                if not self.nodes[node_list[0]].isVisited:
                    break
                node_list.pop(0)
                node_size -= 1
            if node_size <= 0:
                break
            current = node_list.pop(0)
            self.nodes[current].isVisited = True
            if current not in [self.start, self.target]:
                self.nodes[current].visit()
            
            for i, j in self.nodes[current].neighbors:
                neighbor = self.nodes[i*COLUMN + j]
                if not neighbor.isVisited and not neighbor.isObstacle:
                    local_goal = distance(self.nodes[current], neighbor) + self.nodes[current].localGoal
                    if local_goal < neighbor.localGoal:
                        neighbor.parent = current
                        neighbor.localGoal = local_goal
                        neighbor.globalGoal = local_goal + distance(neighbor, self.nodes[self.target])
                    self.nodes[i*COLUMN + j] = neighbor
                    node_list.append(i*COLUMN + j)
            if self.target in node_list and self.stopWhenFind:
                break
            node_size = len(node_list)   
            
                         
        current = self.nodes[self.target]
        
        while current.parent is not None:
            self.path.append(current.parent)
            prev = current
            current = self.nodes[current.parent]
            current.click4(prev)
    
def main():
    
    nodes = []
    
    root = tk.Tk()
    root.resizable(width=False, height=False)
    root.configure(bg='black')
    root.geometry(f"{WIDTH+OFFSET}x{HEIGHT+OFFSET}")
    
    msg = tk.messagebox.askquestion ('Stop when reached to target', "A* algorithm nolmally will visit each node, if you accept this, it will terminate when it finds the target location", icon = 'question')

    ui = UI(msg == "yes")
    
    root.mainloop()



if __name__=="__main__":
    main()
