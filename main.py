from flet import *
from requisicao import principal

def main(page: Page):
    
    page.padding = 0
    page.window.always_on_top = True
    page.window.width = 380
    page.window.height = 710
    page.theme_mode = ThemeMode.DARK
    # page.window.center()
    
    # Titulo do aplicativo
    page.appbar = AppBar(title=Text(value="System Find Product", weight=FontWeight.BOLD), center_title=True, bgcolor='red')
    snack_bar = SnackBar(Text(value='Digite um produto.'))
    page.overlay.append(snack_bar)
    # Função para trocar de janela
    def changeWindow(e):
        index = e.control.selected_index
        window_home.visible = True if index == 0 else False
        window_pesquisar.visible = True if index == 1 else False
        window_dados.visible = True if index == 2 else False
        window_sobre.visible = True if index == 3 else False
        page.update()
    inicio = NavigationBarDestination(icon=icons.HOME, label='Inicio', tooltip='Inicio')
    pesquisar = NavigationBarDestination(icon=icons.SEARCH, label='Pesquisar', tooltip='Pesquisar')
    dados = NavigationBarDestination(icon=icons.DESCRIPTION, label='Dados', tooltip='Dados')
    sobre = NavigationBarDestination(icon=icons.INFO, label='Sobre', tooltip='Sobre')
    page.navigation_bar = NavigationBar(
        selected_index= 0,
        destinations=[inicio,pesquisar,dados,sobre],
        bgcolor='red',
        overlay_color='white',
        surface_tint_color='white',
        indicator_color='blue',
        on_change=changeWindow
    )

    # Pagina Inicial
    imagem = Image(src='assets/1.gif', width=450)
    txt = Text(value='Faça uma pesquisa para saber os menores preços dos produtos que você deseja!',
               text_align=TextAlign.CENTER,
               weight=FontWeight.BOLD,
               size=20
               )
    window_home = ResponsiveRow([
        Container(
            height=1000,  # altura
            width=350,  # Largura
            bgcolor='Red',
            content=Container(
                Column([
                    imagem,
                    txt
                ], horizontal_alignment=CrossAxisAlignment.CENTER)
            )
        )
    ])
        
    # Pagina de Pesquisa
    def abirNot(e):
        page.open(notificacao)
        page.update()
    def fecharNot(e):
        page.close(notificacao)
        page.update()
    def fazerPesquisa(e):
        valor_pesquisa = pesquisa.value
        if not valor_pesquisa:
            snack_bar.open = True
            page.update()
        
        lista.controls.clear()
        bot = principal(usuario=valor_pesquisa)
        resultado = bot.inicio()

        for nome, preco in resultado:
            print(nome)
            print(preco, "\n")
            lista.controls.append(
                Container(
                content=Column([
                    Text(value=nome),
                    Text(value=preco)
                ])
            )
            )
            
        page.update()
    def filtrar(e):
        pass
    lista = GridView(
        expand=1,
        runs_count=5,
        max_extent=200,
        child_aspect_ratio=1.0,
        spacing=50,
        run_spacing=5,
    )
    pesquisa = TextField(width=250, height=45, border_radius=20,
                         color='white', text_align=TextAlign.CENTER, text_vertical_align=VerticalAlignment.CENTER ,hint_text='O que você está procurando?', border_color='white'
                         )
    botão_pesquisar = IconButton(
        icon=icons.SEND, hover_color='green', on_click=fazerPesquisa)
    filtro = RadioGroup(content=Column([
        Radio(value='Preço: do menor para o maior', label='Preço: do menor para o maior'),
        Radio(value='Preço: do maior para o menor', label='Preço: do maior para o menor')
    ]))
    notificacao = BottomSheet(content=Container(
        padding=50,
        content=Column([
            filtro,
            ElevatedButton(text="Aplicar", on_click=fecharNot)
        ], tight=True)
    ))
    window_pesquisar = ResponsiveRow([
        Container(
            height=1000,  # altura
            width=350,  # Largura
            bgcolor='Red',
            content=Container(
                Column([
                    Container(
                        Row([pesquisa,botão_pesquisar], alignment=MainAxisAlignment.CENTER)
                    ),
                    Container(
                        width=350,
                        height=470,
                        bgcolor=colors.BLACK12,
                        border_radius=10,
                        content=Container(
                            Column([
                                IconButton(icon=icons.FILTER_LIST, on_click=abirNot),
                                lista
                            ],horizontal_alignment=CrossAxisAlignment.END)
                        )
                    )
                ],horizontal_alignment=CrossAxisAlignment.CENTER )
            )
        )
    ])
    
    # Pagina de dados
    filtro = RadioGroup(content=Column([
        Radio(value='Preço: do menor para o maior',
              label='Preço: do menor para o maior'),
        Radio(value='Preço: do maior para o menor',
              label='Preço: do maior para o menor')
    ]))
    notificacao = BottomSheet(content=Container(
        padding=50,
        content=Column([
            filtro,
            ElevatedButton(text="Aplicar", on_click=fecharNot)
        ], tight=True)
    ))
    window_dados = ResponsiveRow([
        Container(
            height=1000,  # altura
            width=350,  # Largura
            bgcolor='Red',
            content=Container(
                Column([
                    Container(
                        width=350,
                        height=530,
                        bgcolor=colors.BLACK12,
                        border_radius=10,
                        content=Container(
                            Column([
                                Row([
                                    IconButton(icon=icons.FILTER_LIST, on_click=abirNot),
                                    IconButton(icon=icons.DELETE)
                                ], alignment=MainAxisAlignment.END)
                            ], horizontal_alignment=CrossAxisAlignment.END)
                        )
                    )
                ], horizontal_alignment=CrossAxisAlignment.CENTER)
            )
        )
    ])
    
    # Pagina Sobre
    sobre_image = Image(src='assets/4.gif')
    txt_sobre = Text(value="Eu desenvolvi esse aplicativo, porque eu senti a necessidade de ter um app sempre na mão para fazer pesquisas e comparativos de preço",
                     weight=FontWeight.BOLD, size=20, text_align=TextAlign.CENTER) 
    gitHub = Image(src='assets/GitHub.png', width=100, color='white')
    window_sobre = ResponsiveRow([
        Container(
            height=1000,  # altura
            width=350,  # Largura
            bgcolor='Red',
            content=Container(
                Column([
                    Container(
                        width=350,
                        height=530,
                        bgcolor=colors.BLACK12,
                        border_radius=10,
                        content=Container(
                            padding=padding.only(top=50),
                            content=Column([
                                txt_sobre,
                                Container(
                                    padding=padding.only(top=150),
                                    content=Container(
                                        Row([Text(value='Veja mais Projetos!')],alignment=MainAxisAlignment.CENTER)
                                    )
                                ),
                                Row([
                                    Column([
                                        gitHub, 
                                        TextButton(text='GITHUB', url='https://github.com/RafaelLacerda15'),
                                    ], horizontal_alignment=CrossAxisAlignment.CENTER)
                                ], alignment=MainAxisAlignment.CENTER),
                            ])
                        )
                    )
                ], horizontal_alignment=CrossAxisAlignment.CENTER)
            )
        )
    ])
    
    page.add(window_home, window_pesquisar, window_dados, window_sobre)
    
app(target=main, port=80)