import logging

from Tkinter import *
from tviz.tvizdriver import TvizDriver
from paths import html_file
import webbrowser

DEFAULT_PAD = 3

class TvizGUI:
    


    def __init__(self):
        self.tk = tk = Tk()
        self.ui = ui = TvizUI(self)

        # Mode   
             
        modef = Frame(tk)
        self.tviz_mode = IntVar()
        modef.pack()
        

        row1 = Frame()
        row1.pack(anchor='w')
     
        messagef = Frame()
        messagef.pack(anchor = 'w')

        adminf = Frame(tk)
        adminf.pack(anchor='sw')
        
        self.openbrowser = Button(row1, text = "Open Browser", command = ui.open_browser)
        self.showtanda = Button(row1, text = "Display Tanda", command = ui.run)
        self.message_send = Button(messagef, text = "Display Message", command = ui.send_message)
        
        self.message_txt = StringVar()
        
        self.message_entry = Entry(messagef, textvariable=self.message_txt)
        
        self.quitbutton = Button(adminf, text = "Configure...", command = ui.configure)
        self.quitbutton = Button(adminf, text = "Quit", command = ui.quit)


        self.openbrowser.pack(  side = LEFT, padx = DEFAULT_PAD, pady = DEFAULT_PAD, anchor = 'w')
        self.showtanda.pack(    side = LEFT, padx = DEFAULT_PAD, pady = DEFAULT_PAD, anchor = 'w')
        self.message_send.pack( side = LEFT, padx = DEFAULT_PAD, pady = DEFAULT_PAD, anchor = 'w')
        self.message_entry.pack(  side = LEFT, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        self.quitbutton.pack(   side = LEFT, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        self.quitbutton.pack(   side = LEFT, padx = DEFAULT_PAD, pady = DEFAULT_PAD)
        
        self.ui.send_message('ready')    

        self.tk.mainloop()


class TvizUI:
    
    TVIZ_MODE_OFF = TvizDriver.TVIZ_MODE_OFF
    TVIZ_MODE_MESSAGE = TvizDriver.TVIZ_MODE_MESSAGE
    TVIZ_MODE_TANDA = TvizDriver.TVIZ_MODE_TANDA

    def __init__(self, gui):
        self.gui = gui
        self.tviz = TvizDriver(widget = self)

   
    def run(self):
        self.set_mode(self.TVIZ_MODE_TANDA)
        self._run_loop()

    def _run_loop(self):
        if self.gui.tviz_mode == self.TVIZ_MODE_TANDA:
            logging.info("Starting Tviz from tkui") 
            self.tviz_safe_run_one()
            self.gui.tk.after(3000, self._run_loop)
    
    def open_browser(self):
        webbrowser.open(html_file('index.html'), new=0, autoraise=True)

    def quit(self):
        logging.info("Quiting Tviz from Tkui")
        quit()
  
    def send_message(self, message_override=None):
        if message_override:
            self.gui.message_txt.set(message_override)
        
        self.set_mode(self.TVIZ_MODE_MESSAGE)   
        message = self.gui.message_txt.get()

        self.tviz.setMessage(message)
        self.tviz_safe_run_one()
        
    def tviz_safe_run_one(self):
        try:
            self.tviz.run_one()
        except Exception as e:
            print "TVIZ TERMINATED"
            logging.error('Bad Tviz response: ' + str(e))
            logging.info('Entering Termination Mode')
            self.send_message(' ')
        
    def configure(self):
        logging.info("Will Enter into Config mode")
      
    def set_mode(self, mode):
        logging.debug("Setting mode: " + str(mode))
        self.tviz.setMode(mode)
        self.gui.tviz_mode = mode

if __name__ == '__main__':
    TvizGUI()

