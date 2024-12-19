from selenium.webdriver import Chrome
from Adlib.funcoes import *
from Adlib.api import *
from time import sleep
from Adlib.integracao import loginVirtaus


class FiltrosSolicitacao:

    AGUARDANDO_AVERBACAO = "Aguardando Averbação | AnaliseAverbacao"
    AGUARDANDO_SENHA_BANCO = "Aguardando Senha do Banco | EmissaoDeNovaSenhaLoginExterno"
    AGUARDANDO_TERCEIROS = "Aguardando Terceiros | Notificacao Pagamento Devolvido"
    ANALISA_RECLAMACAO = "Analisa Reclamacao | Criacao de Eventos Reclamacao"
    ANALISAR_CONTRATO_NO_BANCO = "AnalisarContratoNoBanco | AnaliseDaMonitoria"
    ANALISE = "Analise | AnaliseAverbacao"
    ATENDE_AGUARDANDO_TERCEIROS = "Atende Aguardando Terceiros | Criacao de Eventos Reclamacao"
    ATENDIMENTO_ALTERACAO_STATUS_LOGIN = "Atendimento | AlteracaoDoStatusDeLogin"
    CRIACAO = "Atendimento | CriacaoDeLoginExternoParaParceiro"
    RESET = "Atendimento | EmissaoDeNovaSenhaLoginExterno"
    ATENDIMENTO_EMISSAO_NOVA_SENHA_FUNCIONARIO = "Atendimento | EmissaoDeNovaSenhaLoginExternoFuncionario"
    LIBERAR_PROPOSTA = "Liberar Proposta"


def assumirSolicitacao(virtaus: Chrome, nomeFerramenta: str, enumBanco: EnumBanco, tipoFiltro: FiltrosSolicitacao, HORA_FINALIZACAO: str = "19:00"):
    """
        Função para assumir uma solicitação no sistema Virtaus com base em filtros específicos e nome da ferramenta.

        Esta função realiza o seguinte fluxo:
        - Navega para a página de tarefas centralizadas no sistema Virtaus.
        - Seleciona um filtro específico fornecido no parâmetro `tipoFiltro`.
        - Busca pelo nome da ferramenta no campo de pesquisa.
        - Seleciona o primeiro item correspondente à ferramenta.
        - Clica no botão "Assumir Tarefa" para iniciar o processamento.

        Parâmetros:
        - virtaus (Chrome): Instância do navegador Chrome controlada pelo Selenium.
        - nomeFerramenta (str): Nome da ferramenta para buscar nas solicitações.
        - enumBanco (EnumBanco): Enumeração que identifica o banco associado à solicitação.
        - tipoFiltro (FiltrosSolicitacao): Filtro a ser utilizado para categorizar as solicitações.
        - HORA_FINALIZACAO (str): Horário limite para finalizar a execução da função (padrão: "19:00").

        Exceções:
        - A função trata exceções durante a execução, exibindo mensagens informativas e aguardando para novas tentativas.
    """
    while True:

        try:
            virtaus.get("https://adpromotora.virtaus.com.br/portal/p/ad/pagecentraltask")
            qntBotoes = len(esperarElementos(virtaus, '//*[@id="centralTaskMenu"]/li'))
            idxBtn = qntBotoes - 1
            
            clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/a').click()
            
            print(f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/ul//a[contains(text(), "{tipoFiltro}")]')

            # Seleciona o filtro de "Emissão De Nova Senha Login Externo"
            clickarElemento(virtaus, f'//*[@id="centralTaskMenu"]/li[{idxBtn}]/ul//a[contains(text(), "{tipoFiltro}")]').click()

            # Busca pelo nome da ferramenta
            esperarElemento(virtaus, '//*[@id="inputSearchFilter"]').send_keys(nomeFerramenta)

            # Clica no primeira item da lista de solicitações
            clickarElemento(virtaus, f"//td[contains(@title, '{nomeFerramenta}')]").click()
            break

        except Exception as e:
            print(e)
            hora = datetime.datetime.now().strftime("%H:%M")
            print(f"Não há solicitações do banco {nomeFerramenta.title()} no momento {hora}")

            if HORA_FINALIZACAO == hora:
                putRequestFunction(EnumStatus.DESLIGADO, EnumProcesso.RESET, enumBanco)
                sys.exit()

            sleep(30)
    
    try:
        print("Assumindo Tarefa")
        # Clica em Assumir Tarefa e vai para o menu de Cadastro de usuário
        clickarElemento(virtaus, '//*[@id="workflowActions"]/button[1]').click()
    
    except:
        print("Erro ao assumir tarefa")



if __name__=="__main__":
    
    userVirtaus, senhaVirtaus = getCredenciais(160)
    
    driver = setupDriver(r"C:\Users\dannilo.costa\documents\chromedriver.exe")
    
    loginVirtaus(driver, userVirtaus, senhaVirtaus)

    assumirSolicitacao(driver, "CREFISA", EnumBanco.CREFISA, FiltrosSolicitacao.RESET)