from abc import abstractmethod
from genericpath import isdir
from typing import List
from os import getenv, curdir
from os.path import isfile, join

from visualizador.modelos.log import Log
from visualizador.utils.singleton import Singleton


class Configuracoes(metaclass=Singleton):
    """
    Configurações para o visualizador de estudos encadeados.
    """
    def __init__(self) -> None:
        self._porta_servidor = None
        self._periodo_atualizacao_graficos = None
        self._periodo_atualizacao_caso_atual = None
        self._caminhos_casos = None

    @property
    def porta_servidor(self) -> int:
        """
        Porta para hospedar o servidor da aplicação de visualização.

        :return: Número da porta
        :rtype: int
        """
        return self._porta_servidor

    @property
    def periodo_atualizacao_graficos(self) -> float:
        """
        Intervalo entre requisições para leitura dos dados de gráficos
        atualizados em milissegundos.

        :return: Intervalo entre duas leituras consecutivas dos dados (ms)
        :rtype: float
        """
        return self._periodo_atualizacao_graficos

    @property
    def periodo_atualizacao_caso_atual(self) -> float:
        """
        Intervalo entre requisições para leitura dos dados dos casos em
        execução atualizados em milissegundos.

        :return: Intervalo entre duas leituras consecutivas dos dados (ms)
        :rtype: float
        """
        return self._periodo_atualizacao_caso_atual

    @property
    def caminhos_casos(self) -> List[str]:
        """
        Caminhos absolutos até os diretórios raiz onde estão os
        casos encadeados a serem observados

        :return: Caminhos absolutos em unix-style
        :rtype: List[str]
        """
        return self._caminhos_casos

    @classmethod
    def le_variaveis_ambiente(cls) -> "Configuracoes":
        cb = BuilderConfiguracoesENV()
        var_periodo_graficos = "PERIODO_ATUALIZACAO_GRAFICOS"
        var_periodo_caso = "PERIODO_ATUALIZACAO_CASO_ATUAL"
        c = cb.porta_servidor("PORTA_SERVIDOR")\
            .periodo_atualizacao_graficos(var_periodo_graficos)\
            .periodo_atualizacao_caso_atual(var_periodo_caso)\
            .caminhos_casos("CAMINHOS_CASOS")\
            .build()
        return c


class BuilderConfiguracoes:
    """
    Interface genérica para implementação do padrão Builder
    para a classe de Configurações.
    """
    def __init__(self,
                 configuracoes: Configuracoes):
        self._configuracoes = configuracoes
        self._log = Log.log()

    def build(self) -> Configuracoes:
        return self._configuracoes

    @abstractmethod
    def porta_servidor(self, variavel: str):
        pass

    @abstractmethod
    def periodo_atualizacao_graficos(self, variavel: str):
        pass

    @abstractmethod
    def periodo_atualizacao_caso_atual(self, variavel: str):
        pass

    @abstractmethod
    def caminhos_casos(self, variavel: str):
        pass


class BuilderConfiguracoesENV(BuilderConfiguracoes):
    """
    Implementação do padrão builder para as configurações,
    no caso da construção a partir de variáveis de ambiente.
    """
    def __init__(self,
                 configuracoes: Configuracoes=Configuracoes()):
        super().__init__(configuracoes=configuracoes)

    @staticmethod
    def __le_e_confere_variavel(variavel: str):
        # Lê a variável de ambiente
        valor = getenv(variavel)
        # Valida o conteúdo
        if valor is None:
            raise ValueError(f"Variável {variavel} não encontrada")
        return valor

    @staticmethod
    def __valida_int(variavel: str):
        try:
            valor = int(variavel)
            valorfloat = float(variavel)
            if valor != valorfloat:
                raise ValueError()
        except ValueError:
            raise ValueError(f"Variável {variavel} não é inteira")
        return valor

    @staticmethod
    def __valida_float(variavel: str):
        try:
            valor = float(variavel)
        except ValueError:
            raise ValueError(f"Variável {variavel} não é real")
        return valor

    def porta_servidor(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        valor = BuilderConfiguracoesENV.__valida_int(valor)
        if not (1024 <= valor <= 65535):
            raise ValueError("A porta fornecida deve estar no intervalo" +
                             " [1024, 65535].")
        self._configuracoes._porta_servidor = valor
        # Fluent method
        self._log.info(f"Porta do servidor: {valor}")
        return self

    def periodo_atualizacao_graficos(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        valor = BuilderConfiguracoesENV.__valida_float(valor)
        if valor <= 0:
            raise ValueError("O período de atualização deve ser > 0. " +
                             f"Fornecido: {valor}")
        self._configuracoes._periodo_atualizacao_graficos = valor
        # Fluent method
        self._log.info(f"Período de atualização de gráficos: {valor}")
        return self

    def periodo_atualizacao_caso_atual(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        valor = BuilderConfiguracoesENV.__valida_float(valor)
        if valor <= 0:
            raise ValueError("O período de atualização deve ser > 0. " +
                             f"Fornecido: {valor}")
        self._configuracoes._periodo_atualizacao_caso_atual = valor
        # Fluent method
        self._log.info(f"Período de atualização do caso atual: {valor}")
        return self

    def caminhos_casos(self, variavel: str):
        valor = BuilderConfiguracoesENV.__le_e_confere_variavel(variavel)
        # Confere se os caminhos são válidos
        valor = valor.split(',')
        if not all([len(c) > 0 for c in valor]):
            raise ValueError(f"Os caminhos informados {valor} são" +
                             f" inválidos. Não podem ser vazios.")
        for c in valor:
            if not isdir(c):
                raise ValueError(f"O caminho {c} não é um diretório.")
        self._configuracoes._caminhos_casos = valor
        # Fluent method
        self._log.info(f"Caminhos dos casos: {valor}")
        return self
