from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image 

class MenuPrincipal(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.rows = 5
        self.add_widget(self.titulo)
        self.add_widget(self.continuar_botao_visual)
        self.add_widget(self.iniciar_botao_visual)
        self.add_widget(self.produtividade_botao_visual)
        self.add_widget(self.sair_botao_visual)
        


    @property
    def titulo(self):
        titulo = Image(source="POM.png")   
        return titulo

    @property
    def continuar_botao_visual(self):
        botao = Button(text='Continuar')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        return botao   
    
    @property
    def iniciar_botao_visual(self):
        botao = Button(text='Iniciar')
        botao.bold = True
        botao.font_size = 20 
        botao.background_color = [1,2,3,4]
        botao.bind(on_press=self.iniciar_botao_func)
        return botao
    @property    
    def produtividade_botao_visual(self):
        botao = Button(text='Produtividade')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        return botao        
    
    @property
    def sair_botao_visual(self):
        botao = Button(text='Sair')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        botao.bind(on_press=self.sair_botao_func)
        return botao     
      
    def iniciar_botao_func(self, instance):
        pom.screen_manager.current = "Iniciar"
    
    def sair_botao_func(self, instance):
        pom.stop()

class TelaIniciar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols= 1
        self.add_widget(Label(text='META'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)


class Pom(App):

    def build(self):
        
        self.screen_manager = ScreenManager()

        self.menu_principal = MenuPrincipal()
        screen = Screen(name="Menu")
        screen.add_widget(self.menu_principal)
        self.screen_manager.add_widget(screen)

        self.iniciar = TelaIniciar()
        screen = Screen(name="Iniciar" )
        screen.add_widget(self.iniciar)
        self.screen_manager.add_widget(screen)
        Window.clearcolor = (1, 2, 3, 4)
        return self.screen_manager


if __name__ == '__main__':
    pom = Pom()
    pom.run()   































































































