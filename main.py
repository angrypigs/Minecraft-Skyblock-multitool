import pyautogui as pg
import tkinter as tk
import time as tm
from pynput.keyboard import Key, Listener
from pynput import keyboard

flag_working = False

class cobblestoneMiner:
    """
    Class with cobblestone miner functions
    """

    def __init__(self) -> None:
        pass

    def time_counter(self, seconds: int) -> None:
        counter = 0
        while counter < seconds:
            tm.sleep(1)
            if not flag_working:
                return
            counter += 1

    def mine(self, time: int = 197) -> None:
        if not flag_working:
            return
        pg.mouseDown(button='left')
        self.time_counter(time)
        pg.mouseUp(button='left')

    def start(self, coords: list, pickaxe_amount: int) -> None:
        self.FIRST_CELL = [coords[0], coords[1]]
        self.DIST = coords[2]
        self.mine()
        for i in range(pickaxe_amount):
            if not flag_working:
                return
            pg.press('e')
            pg.moveTo(self.FIRST_CELL[0]+(i%9*self.DIST), self.FIRST_CELL[1]+(i//9*self.DIST))
            pg.press('1')
            pg.press('esc')
            pg.press('1')
            self.mine()



class coarseDirtMiner:
    """
    Class with coarse dirt miner functions
    """

    def __init__(self) -> None:
        pass

    def mine(self, time_delay: float = 0.4) -> None:
        pg.press('1')
        pg.click(button='right')
        pg.press('2')
        pg.click(button='right')
        pg.mouseDown(button='left')
        tm.sleep(time_delay)
        pg.mouseUp(button='left')
    
    def reload(self, idx: int) -> int:
        pg.press('2')
        pg.press('q')
        pg.keyDown('shiftleft')
        pg.press('e')
        pg.moveTo(self.FIRST_CELL[0]+(idx%9*self.DIST), self.FIRST_CELL[1]+(idx//9*self.DIST))
        pg.rightClick(self.FIRST_CELL[0]+(idx%9*self.DIST), self.FIRST_CELL[1]+(idx//9*self.DIST))
        idx += 1
        pg.moveTo(self.FIRST_CELL[0]+(idx%9*self.DIST), self.FIRST_CELL[1]+(idx//9*self.DIST))
        pg.rightClick(self.FIRST_CELL[0]+(idx%9*self.DIST), self.FIRST_CELL[1]+(idx//9*self.DIST))
        idx += 1
        pg.keyUp('shiftleft')
        pg.press('esc')
        return idx
    
    def start(self, coords: list) -> None:
        self.FIRST_CELL = [coords[0], coords[1]]
        self.DIST = coords[2]
        index = 0
        counter = 0
        while True:
            if not flag_working:
                return
            counter += 1
            self.mine()
            if counter%64==0:
                index = self.reload(index)



class autoBridge:
    """
    Class with auto bridge functions
    """
    def __init__(self) -> None:
        pass
    
    def start(self) -> None:
        pg.keyDown('shiftleft')
        pg.keyDown('s')
        tm.sleep(0.5)
        pg.rightClick()
        while True:
            if not flag_working:
                pg.keyUp('s')
                pg.rightClick()
                pg.keyUp('shiftleft')
                return
            tm.sleep(0.65)
            pg.rightClick()
        
        

class App:
    """
    App class
    """
    def __init__(self) -> None:
        # init constants
        self.HEIGHT = 350
        self.WIDTH = 300
        self.EQ_COORDS_LIST = [[], [670, 575, 72], [840, 780, 108]]
        # init app
        self.master = tk.Tk()
        self.mode = tk.IntVar(self.master, value=1)
        self.resolution = tk.IntVar(self.master, value=2)
        self.master.title("Minecraft multitool")
        self.master.geometry("{}x{}".format(self.WIDTH, self.HEIGHT))
        self.master.resizable(False, False)
        c_main = tk.Canvas(self.master, height=self.HEIGHT, width=self.WIDTH, bd=0, highlightthickness=0, bg="#EEC2A2")
        c_main.place(x=0, y=0)
        checkbox1 = tk.Radiobutton(c_main, text="Coarse dirt to dirt converter", variable=self.mode, value=1, bg="#EEC2A2", font=16)
        checkbox1.place(x=10, y=20)
        checkbox2 = tk.Radiobutton(c_main, text="Cobblestone miner", variable=self.mode, value=2, bg="#EEC2A2", font=16)
        checkbox2.place(x=10, y=50)
        checkbox3 = tk.Radiobutton(c_main, text="Auto bridge", variable=self.mode, value=3, bg="#EEC2A2", font=16)
        checkbox3.place(x=10, y=80)
        # start listening for keys
        self.key_listen()
        self.master.mainloop()
    
    def key_listen(self) -> None:
        # function to listen for keys
        self.listener = Listener(on_press=self.choose_program)
        self.listener.start()

    def choose_program(self, key) -> None:
        global flag_working
        if key == keyboard.Key.f6 and not flag_working:
            if self.mode.get()==1:
                flag_working = True
                self.key_listen()
                coarseDirtMiner().start(self.EQ_COORDS_LIST[self.resolution.get()])
            elif self.mode.get()==2:
                flag_working = True
                self.key_listen()
                cobblestoneMiner().start(self.EQ_COORDS_LIST[self.resolution.get()], 9)
            elif self.mode.get()==3:
                flag_working = True
                self.key_listen()
                autoBridge().start()
        if key == keyboard.Key.f7:
            self.listener.stop()
            flag_working = False



if __name__ == "__main__":
    app = App()
    