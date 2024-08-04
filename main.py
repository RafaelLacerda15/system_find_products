from flet import *
from requisicao import principal
from banco_dados import bd

def main(page: Page):
    
    page.padding = 0
    page.window.always_on_top = True
    page.window.width = 380
    page.window.height = 710
    
    page.window.min_width = 380
    page.window.min_height = 710
    page.theme_mode = ThemeMode.DARK
    # page.window.center()
    
    # Titulo do aplicativo
    page.appbar = AppBar(title=Text(value="System Find Product", weight=FontWeight.BOLD), center_title=True, bgcolor='red')
    
    # Notificação
    snack_bar = SnackBar(Text(value='Digite um produto.'))
    page.overlay.append(snack_bar)
    
    snack_bar2 = SnackBar(Text(value='Lista Vazia!'))
    page.overlay.append(snack_bar2)
    
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
        contador = 0
        texto_resultado.visible = True
        lista.controls.clear()
        bot = principal(usuario=valor_pesquisa)
        resultado = bot.inicio()
        
        for nome, preco, link, site in resultado:
            contador += 1
            lista.controls.append(
                Container(
                    bgcolor=colors.WHITE12,
                    border_radius=15,
                    content=Column([
                        Text(value=f'{contador}: {nome}', text_align=TextAlign.CENTER, color='white'),
                        Text(value=preco, text_align=TextAlign.CENTER, color='white'),
                        TextButton(text=site, url=link, style=ButtonStyle(color='white',bgcolor='blue'))
                    ], horizontal_alignment=CrossAxisAlignment.CENTER)
                )
            )
            
        page.update()
    def clearList(e):
        texto_resultado.visible = False
        lista.controls.clear()
        page.update()
    def filtrar(e):
            evento = e.control
            if evento.value == '1':
                print(f'Escolheu o valor: {evento}')
            elif evento.value == '2':
                print(f'Escolheu o valor: {evento}')
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
    texto_resultado = Text(value='Resultado', weight=FontWeight.BOLD)
    texto_resultado.visible = False
    botão_pesquisar = IconButton(
        icon=icons.SEND, hover_color='green', on_click=fazerPesquisa, tooltip='Pesquisar')
    filtro = RadioGroup(content=Column([
        Radio(value='1', label='Preço: do menor para o maior'),
        Radio(value='2', label='Preço: do maior para o menor')
    ]), on_change=filtrar)
    notificacao = BottomSheet(content=Container(
        padding=50,
        content=Column([
            filtro
        ], tight=True)
    ))
    window_pesquisar = ResponsiveRow([
        Container(
            height=1000,  # altura
            width=350,  # Largura
            bgcolor='Red',
            content=ResponsiveRow([
                Container(
                    Column([
                        Container(
                            Row([pesquisa, botão_pesquisar],
                                alignment=MainAxisAlignment.CENTER)
                        ),
                        ResponsiveRow([
                            Container(
                                width=350,
                                height=470,
                                bgcolor=colors.BLACK12,
                                border_radius=10,
                                content=Container(
                                    Column([
                                        Container(
                                            Row([
                                                texto_resultado,
                                                Container(width=100),
                                                IconButton(icon=icons.CLEAR_ALL, on_click=clearList, tooltip='Limpar lista'),
                                                IconButton(icon=icons.FILTER_LIST, on_click=abirNot, tooltip='Filtrar'),
                                            ],alignment=MainAxisAlignment.END)
                                        ),
                                        lista
                                    ], horizontal_alignment=CrossAxisAlignment.END)
                                )
                            )
                        ])
                    ], horizontal_alignment=CrossAxisAlignment.CENTER)
                )
            ])
        )
    ])
    
    # Pagina de dados
    def exibirPesquisa(e):
        exibir = bd()
        resultado = exibir.selectAll()
        contador = 0
        itens_exibidos = set()
        if not resultado:
            snack_bar2.open = True
            
        for nome, preco, link, site in resultado:
            if nome not in itens_exibidos:
                contador += 1
                lista2.controls.append(
                    Container(
                        bgcolor=colors.WHITE12,
                        border_radius=15,
                        content=Column([
                            Text(value=f'{contador}: {nome}', text_align=TextAlign.CENTER, color='white'),
                            Text(value=preco, text_align=TextAlign.CENTER, color='white'),
                            TextButton(text=site, url=link, style=ButtonStyle(color='white', bgcolor='blue'))
                        ], horizontal_alignment=CrossAxisAlignment.CENTER)
                    )
                )
                itens_exibidos.add(nome)
        
        page.update()
    def deletBase(e):
        exibir = bd()
        deletar = exibir.deletarBanco()
        
        lista2.controls.clear()
        page.update()
    
    lista2 = GridView(
        expand=1,
        runs_count=5,
        max_extent=200,
        child_aspect_ratio=1.0,
        spacing=50,
        run_spacing=5,
        
    )
    filtro = RadioGroup(content=Column([
        Radio(value='1', label='Preço: do menor para o maior'),
        Radio(value='2', label='Preço: do maior para o menor')
    ]), on_change=filtrar)
    notificacao = BottomSheet(content=Container(
        padding=50,
        content=Column([
            filtro
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
                                    IconButton(icon=icons.VISIBILITY, on_click=exibirPesquisa, tooltip='Mostrar Dados'),
                                    IconButton(icon=icons.FILTER_LIST, on_click=abirNot, tooltip='Filtrar'),
                                    IconButton(icon=icons.DELETE, on_click=deletBase, tooltip='Deletar Dados')
                                ], alignment=MainAxisAlignment.END),
                                lista2
                            ], horizontal_alignment=CrossAxisAlignment.END)
                        )
                    )
                ], horizontal_alignment=CrossAxisAlignment.CENTER)
            )
        )
    ])
    
    # Pagina Sobre 
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
    
    page.add(window_home,
             window_pesquisar,
             window_dados,
             window_sobre
            )
    
app(target=main)