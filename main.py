from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput  
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.image import Image 
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import  NumericProperty
from crud import Crud, Grafico

class MenuPrincipal(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pom.crud.conectar()
        self.banco = pom.crud.read()
        pom.crud.close

        self.rows = 5
        self.add_widget(self.titulo)
        if not self.banco==None:
            self.add_widget(self.continuar_botao)
        self.add_widget(self.iniciar_botao)
        self.add_widget(self.produtividade_botao)
        self.add_widget(self.sair_botao)
        


    @property
    def titulo(self):
        titulo = Image(source="POM.png")   
        return titulo

    @property
    def continuar_botao(self):
        botao = Button(text='Continuar')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        return botao   
    
    @property
    def iniciar_botao(self):
        botao = Button(text='Iniciar')
        botao.bold = True
        botao.font_size = 20 
        botao.background_color = [1,2,3,4]
        botao.bind(on_press=self.iniciar_botao_func)
        return botao
    @property    
    def produtividade_botao(self):
        botao = Button(text='Produtividade')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        botao.bind(on_press=self.produtividade_botao_func)
        return botao        
    
    @property
    def sair_botao(self):
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

    def produtividade_botao_func(self, instance):        
        try:
            pom.screen_manager.current = "Produtividade"
            pom.produtividade.grafico()
        except Exception as e:
            print("erro:", e)

    def continuar_botao_func(self, instance):
        self.pomodoro_continuar = Pomodoro(continuar=True)
        pom.continuar = self.pomodoro.continuar
        screen = Screen(name="Continuar")
        screen.add_widget(self.pomodoro)
        pom.screen_manager.add_widget(screen)
        pom.screen_manager.current = "Pomodoro"

class TelaIniciar(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spacing=(0,7)
        self.cols = 2
        self.rows = 4        
        self.meta = self.meta_input()
        self.qtd_dias = self.qtd_dias_input()
        self.tempo_dia = self.tempo_dia_input()
        self.voltar_botao()
        self.botao_submeter()
        

    def meta_input(self):
        meta_label = Label(
            text="Meta", 
            color=(0,0,0,1),
            font_size= 20,
            bold = True,            
             )

        meta = TextInput(
            multiline = False,
            font_size = 20,
            )
        self.add_widget(meta_label)        
        self.add_widget(meta)
        return meta

    def qtd_dias_input(self):
        qtd_dias_label = Label(
            text="Número de dias de dedicação", 
            color=(0,0,0,1),
            font_size= 20,
            bold = True )
        qtd_dias = TextInput(
            multiline=False,
            font_size = 20,
            input_filter = 'int'
            )
               
        self.add_widget(qtd_dias_label)
        self.add_widget(qtd_dias)      

        return qtd_dias

    def tempo_dia_input(self):
        tempo_dia_label = Label(
            text = "Tempo por dia dedicado",
            color = (0,0,0,1),
            font_size = 20,
            bold = True)
        tempo_dia = TextInput(
            multiline=False,
            font_size = 20,
            input_filter = 'int')
        
        self.add_widget(tempo_dia_label)
        self.add_widget(tempo_dia)
        return tempo_dia

    def voltar_botao(self):
        botao = Button(text='Voltar')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        botao.bind(on_press=self.voltar_botao_func)
        self.add_widget(botao)

    def voltar_botao_func(self, instance):
        pom.screen_manager.current = "Menu"

    def botao_submeter(self):
        botao = Button(text='Submeter')
        botao.bold = True
        botao.font_size = 20
        botao.background_color = [1,2,3,4]
        botao.bind(on_press=self.submeter_botao_func)
        self.add_widget(botao)
    
    def submeter_botao_func(self, instance):
        meta = self.meta.text
        qtd_dias = self.qtd_dias.text
        tempo_dia = self.tempo_dia.text

        if meta and qtd_dias and tempo_dia:
            qtd_dias = int(qtd_dias)
            tempo_dia = int(tempo_dia)
            try:
                pom.crud.conectar()
                pom.crud.insert(meta=meta, dias= qtd_dias, horas_dias=tempo_dia )
                pom.crud.close()
            except Exception as e:
                print("Erro:", e)
            else:
                self.pomodoro = Pomodoro()
                pom.pomodoro = self.pomodoro
                screen = Screen(name="Pomodoro")
                screen.add_widget(self.pomodoro)
                pom.screen_manager.add_widget(screen)
                pom.screen_manager.current = "Pomodoro"
class Pomodoro(GridLayout):
    def __init__(self, continuar=False,**kwargs):
        super().__init__(**kwargs)
        self.turno = 1
        self.tempo = Temporizador()
        self.cols = 1 
        self.rows = 5
        
        pom.crud.conectar()
        self.indice, self.meta, self.dias, self.horas, self.data_inicio= pom.crud.read()
        self.indice_prod, self.data, self.minutos = pom.crud.read(produtividade=True)
        pom.crud.close()
        
        self.titulo()
        self.comecar_botao()
        self.parar_botao()
        self.retomar_botao()
        self.finalizar_botao()
        self.sessao()

        self.add_widget(self.titulo)
        self.add_widget(self.sessao)
        self.add_widget(self.tempo)
        self.add_widget(self.comecar_botao)
        

    def titulo(self):
        self.titulo = Label(
            text=self.meta,
            color = [0,0,0,1],
            font_size = 25,
            bold = True
            )

    def sessao(self):             
        horas = self.horas
        tempo_dia = horas*60
        self.qtd_sessao = tempo_dia//25
        self.total_dias = self.dias
        self.dia_atual = self.indice_prod
        self.inicio = self.data_inicio
        self.texto1 = f"Data inicio: {self.inicio} \nDias: {self.dia_atual}/{self.total_dias}"
        self.texto2 = f"Turnos: {self.turno}/{self.qtd_sessao}"
        self.sessao = Label(
        text = f"{self.texto1}\n{self.texto2}",
        color = [0,0,0,1],
        font_size = 25,
        bold = True
        )


    def renderizar_tela(self):
        self.clear_widgets()

        self.add_widget(self.titulo)
        self.add_widget(self.sessao)
        self.add_widget(self.tempo)
        self.add_widget(self.parar_botao)

    def temporizador(self):
        if self.turno <= self.qtd_sessao:
            self.tempo = None
            self.tempo = Temporizador()
            self.renderizar_tela()
            self.tempo.start25()

    
    def comecar_botao(self):
        self.comecar_botao = Button(text='Começar')
        self.comecar_botao.bold = True
        self.comecar_botao.font_size = 20
        self.comecar_botao.background_color = [1,2,3,4]
        self.comecar_botao.bind(on_press=self.comecar_botao_func)

    def comecar_botao_func(self, instance):
        self.remove_widget(self.comecar_botao)
        self.add_widget(self.parar_botao)
        self.tempo.start25()

    def parar_botao(self):
        self.parar_botao = Button(text='Parar')
        self.parar_botao.bold = True
        self.parar_botao.font_size = 20
        self.parar_botao.background_color = [1,2,3,4]
        self.parar_botao.bind(on_press=self.parar_botao_func)

    def parar_botao_func(self, instance):
        self.remove_widget(self.parar_botao)
        self.add_widget(self.retomar_botao)
        self.add_widget(self.finalizar_botao)
        self.tempo.parar()

    def retomar_botao(self):
        self.retomar_botao = Button(text='Retomar')
        self.retomar_botao.bold = True
        self.retomar_botao.font_size = 20
        self.retomar_botao.background_color = [1,2,3,4]
        self.retomar_botao.bind(on_press=self.retomar_botao_func)

    def retomar_botao_func(self, instance):
        self.remove_widget(self.retomar_botao)
        self.remove_widget(self.finalizar_botao)
        self.add_widget(self.parar_botao)
        self.tempo.retomar()

    def finalizar_botao(self):
        self.finalizar_botao = Button(text='Finalizar')
        self.finalizar_botao.bold = True
        self.finalizar_botao.font_size = 20
        self.finalizar_botao.background_color = [1,2,3,4]
        self.finalizar_botao.bind(on_press=self.finalizar_botao_func)

    def finalizar_botao_func(self, instance):
        pom.crud.conectar()
        pom.crud.insert(produtividade=True, minutos = self.turno*25, id_inicio = self.indice)        
        pom.screen_manager.current = "Menu"
        


class Temporizador(Label):

    color = [0,0,0,1]
    font_size = 25
    bold = True
    tf25 = NumericProperty(5)
    tf5 = NumericProperty(5)

    def start25(self):
        Animation.cancel_all(self)
        self.anim = Animation(tf25=0, duration=self.tf25)
        
        def fim(animation, instance):
            if pom.pomodoro.turno < pom.pomodoro.qtd_sessao: 
                pom.pomodoro.turno+=1
                texto1 = pom.pomodoro.texto1
                texto2 = f"Turnos: {pom.pomodoro.turno}/{pom.pomodoro.qtd_sessao}"
                pom.pomodoro.sessao.text = f"{texto1}\n{texto2}"
                pom.pomodoro.renderizar_tela()
                self.start5()
            else:
                instance.text = "FIM"
                Clock.schedule_once(pom.pomodoro.finalizar_botao_func, 5)

        self.anim.bind(on_complete=fim)
        self.anim.start(self)
    
    def start5(self):
        Animation.cancel_all(self)
        self.anim = Animation(tf5=0, duration=self.tf5)

        def fim(animation, instance):
            pom.pomodoro.temporizador()

        self.anim.bind(on_complete=fim)
        self.anim.start(self)

    def parar(self):
        self.anim.cancel(self)
    
    def retomar(self):
        self.anim.start(self)

    def on_tf25(self, instance, value):
        self.text = f"{int(value//60)}:{int(value%60)}"

    def on_tf5(self, instance, value):
        self.text = f"{int(value//60)}:{int(value%60)}"

class Produtividade(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

        
    
    def grafico(self):
        self.grafico = Grafico()
        self.grafico.plotar()
        self.grafico_imagem = Image(source="grafico.png") 
        self.grafico.allow_stretch=True 

        self.add_widget(self.grafico_imagem)
        
                

class Pom(App):

    def build(self):

        self.crud = Crud()
        Window.clearcolor = (1, 2, 3, 4)
        self.screen_manager = ScreenManager()

        self.menu_principal = MenuPrincipal()
        screen = Screen(name="Menu")
        screen.add_widget(self.menu_principal)
        self.screen_manager.add_widget(screen)

        self.iniciar = TelaIniciar()
        screen = Screen(name="Iniciar" )
        screen.add_widget(self.iniciar)
        self.screen_manager.add_widget(screen)

        self.produtividade = Produtividade()
        screen = Screen(name="Produtividade")
        screen.add_widget(self.produtividade)
        self.screen_manager.add_widget(screen)

        self.pomodoro = ""
        self.continuar = ""

        return self.screen_manager


if __name__ == '__main__':
    pom = Pom()
    pom.run()   































































































