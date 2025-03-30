import tkinter as tk

class DrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw on Canvas")
        
        self.canvas = tk.Canvas(root, bg="white", width=500, height=500)
        self.canvas.pack()
        
        
        
        self.old_x = None
        self.old_y = None
    
    
        
        self.old_x = event.x
        self.old_y = event.y
    
    def reset(self, event):
        self.old_x = None
        self.old_y = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawApp(root)
    root.mainloop()
