from tkinter import Tk, PhotoImage
from tkinter.ttk import Notebook, Frame, Style, Label, Entry, Button


class NewNotebook(Notebook):  # Herencia (la clase NewNotebook estará derivada de Notebook)

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__initialized = True

        kwargs['style'] = 'NewNotebook'
        Notebook.__init__(self, *args, **kwargs)
        self.__active = None

        self.bind('<ButtonPress-1>', self.close_click, True)
        self.bind('<ButtonRelease-1>', self.close_unclick)

    def close_click(self, event):
        element = self.identify(event.x, event.y)
        if 'close' in element:
            index = self.index('@%d, %d' % (event.x, event.y))
            self.state(['pressed'])
            self._active = index

    def close_unclick(self, event):

        if not self.instate(['pressed']):
            return

        element = self.identify(event.x, event.y)
        index = self.index('@%d, %d' % (event.x, event.y))

        if 'close' in element and self._active == index:
            self.forget(index)
            self.event_generate('<<NotebookTabClosed>>')

        self.state(['!pressed'])
        self._active = None

    def __initialize_custom_style(self):
        style = Style()
        self.images = (
            PhotoImage('img_close', file='close.gif'),
            PhotoImage('img_close_active', file='close_active.gif'),
            PhotoImage('img_close_pressed', file='close_pressed.gif')
        )

        style.element_create('close', 'image', 'img_close',
                             ('active', 'pressed', '!disabled', 'img_close_pressed'),
                             ('active', '!disabled', 'img_close_active'), border=5, sticky='')

        style.layout('NewNotebook', [
                     ('NewNotebook.client', {'sticky': 'nswe'})])
        style.layout('NewNotebook.Tab', [
            ('NewNotebook.tab', {
                'sticky': 'nswe',
                'children': [
                    ('NewNotebook.padding', {
                        'side': 'top',
                        'sticky': 'nswe',
                        'children': [
                            ('NewNotebook.focus', {
                                'side': 'top',
                                'sticky': 'nswe',
                                'children': [
                                    ('NewNotebook.close', {
                                        'side': 'left', 'sticky': ''}),
                                    ('NewNotebook.label', {
                                        'side': 'left', 'sticky': ''})
                                ]
                            })
                        ]
                    })
                ]
            })
        ])


root = Tk()

root.geometry('200x200')
root.title('Pestañas con botón de cierre')

ntbk_close = NewNotebook(root)

frm_1 = Frame(ntbk_close)
Label(frm_1, text='Texto prueba...').pack()
frm_1.pack()

frm_2 = Frame(ntbk_close)
Entry(frm_2).pack()
frm_2.pack()

frm_3 = Frame(ntbk_close)
Button(frm_3, text='Botón de prueba').pack()
frm_3.pack()

ntbk_close.add(frm_1, text='Frame 1')
ntbk_close.add(frm_2, text='Frame 2')
ntbk_close.add(frm_3, text='Frame 3')

ntbk_close.pack()

root.mainloop()
