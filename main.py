import pyautogui as pg
import tkinter as tk
import time as tm
from pynput.keyboard import Key, Listener
from pynput import keyboard

h, w = 350, 300
flag_working = False

class cobblestoneMiner:

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
        for i in range(9):
            if not flag_working:
                return
            pg.mouseDown(button='left')
            self.time_counter(time)
            pg.mouseUp(button='left')
            if i != 8:
                pg.press(str(i+2))
            tm.sleep(1)

    def start(self, pickaxe_amount: int) -> None:
        self.mine()
        for i in range(pickaxe_amount):
            if not flag_working:
                return
            pg.press('e')
            pg.keyDown('shiftleft')
            coords = [670, 575+(i*70)]
            for j in range(9):
                pg.click(coords[0], coords[1])
                coords[0] += 70
            pg.click(coords[0], coords[1])
            pg.keyUp('shiftleft')
            pg.press('esc')
            pg.press('1')
            self.mine()

class coarseDirtMiner:

    def __init__(self) -> None:
        pass

    def mine(self, time: float = 2) -> None:
        pg.press('1')
        pg.click(button='right')
        pg.press('2')
        pg.click(button='right')
        pg.mouseDown(button='left')
        tm.sleep(time)
        pg.mouseUp(button='left')
    
    def reload(self, idx: int) -> int:
        pg.press('2')
        pg.press('q')
        pg.keyDown('shiftleft')
        pg.press('e')
        pg.moveTo(670+(idx%9*70), 575+(idx//9*70))
        pg.rightClick(670+(idx%9*70), 575+(idx//9*70))
        idx += 1
        pg.moveTo(670+(idx%9*70), 575+(idx//9*70))
        pg.rightClick(670+(idx%9*70), 575+(idx//9*70))
        idx += 1
        pg.keyUp('shiftleft')
        pg.press('esc')
        return idx
    
    def start(self, time: float = 2) -> None:
        index = 0
        counter = 0
        while True:
            if not flag_working:
                return
            counter += 1
            self.mine(time)
            if counter%64==0:
                index = self.reload(index)

class App:
    def __init__(self) -> None:
        self.master = tk.Tk()
        self.mode = tk.IntVar()
        self.master.title("Minecraft multitool")
        self.master.geometry("{}x{}".format(w, h))
        self.master.resizable(False, False)
        c_main = tk.Canvas(self.master, height=h, width=w, bd=0, highlightthickness=0, bg="#EEC2A2")
        c_main.place(x=0, y=0)
        checkbox1 = tk.Radiobutton(c_main, text="Coarse dirt to dirt converter", variable=self.mode, value=1, bg="#EEC2A2", font=16)
        checkbox2 = tk.Radiobutton(c_main, text="Cobblestone miner", variable=self.mode, value=2, bg="#EEC2A2", font=16)
        checkbox1.place(x=10, y=20)
        checkbox2.place(x=10, y=50)
        self.key_listen()
        self.master.mainloop()
    
    def key_listen(self) -> None:
        global listener
        listener = Listener(on_press=self.choose_program)
        listener.start()

    def choose_program(self, key) -> None:
        global flag_working
        if key == keyboard.Key.f6 and not flag_working:
            if self.mode.get()==1:
                flag_working = True
                self.key_listen()
                coarseDirtMiner().start(0.4)
            elif self.mode.get()==2:
                flag_working = True
                self.key_listen()
                cobblestoneMiner().start(9)
        if key == keyboard.Key.f7:
            listener.stop()
            flag_working = False

if __name__ == "__main__":
    app = App()
    