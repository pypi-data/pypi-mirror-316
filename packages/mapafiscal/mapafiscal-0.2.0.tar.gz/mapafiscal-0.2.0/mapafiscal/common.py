from enum import Enum, unique
from dataclasses import dataclass


#######################################################################
# Tipos de dados comuns
#######################################################################
 
@unique
class UF(Enum):
    SP = ("SP", "São Paulo")
    MG = ("MG", "Minas Gerais")
    RJ = ("RJ", "Rio de Janeiro")
    ES = ("ES", "Espírito Santo")
    PR = ("PR", "Paraná")
    RS = ("RS", "Rio Grande do Sul")
    SC = ("SC", "Santa Catarina")
    MS = ("MS", "Mato Grosso do Sul")
    MT = ("MT", "Mato Grosso")
    GO = ("GO", "Goiás")
    DF = ("DF", "Distrito Federal")
    AC = ("AC", "Acre")
    AL = ("AL", "Alagoas")
    AM = ("AM", "Amazonas")
    AP = ("AP", "Amapá")
    BA = ("BA", "Bahia")
    CE = ("CE", "Ceará")
    MA = ("MA", "Maranhão")
    PB = ("PB", "Pará")
    PE = ("PE", "Pernambuco")
    PI = ("PI", "Piauí")
    RN = ("RN", "Rio Grande do Norte")
    SE = ("SE", "Sergipe")
    TO = ("TO", "Tocantins")
    RR = ("RR", "Roraima")
    RO = ("RO", "Rondônia")
    PA = ("PA", "Pará")
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")

    @staticmethod
    def list(index = 0):        
        return [elem.value[index] for elem in UF]        

    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def sigla(self):
        return self.value[0]
    
    def __eq__(self, other):
        if isinstance(other, UF):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
  

@unique
class PerfilContribuinte(Enum):
    COMERCIO_VAREJISTA = ("comercio_varejista", "Comércio Varejista")
    COMERCIO_ATACADISTA = ("comercio_atacadista", "Comércio Atacadista")
    IMPORTADOR = ("importador", "Importador")
    FABRICANTE = ("fabricante", "Fabricante")
    PRODUTOR_RURAL = ("produtor_rural", "Produtor Rural")
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
      
    def __eq__(self, other):
        if isinstance(other, PerfilContribuinte):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:    
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")
    
    @staticmethod
    def list(index = 0):
        return [elem[index] for elem in PerfilContribuinte]


@unique
class TipoIncidencia(Enum):
    TRIBUTADO = ("tributado", "Tributado")
    NAO_TRIBUTADO = ("nao_tributado", "Não Tributado")
    ISENTO = ("isento", "Isento")
    SUSPENSO = ("suspenso", "Supenso")
    DIFERIDO = ("diferido", "Diferido")
    RETIDO = ("retido", "Retido")
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
      
    def __eq__(self, other):
        if isinstance(other, TipoIncidencia):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:    
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")
    
    @staticmethod
    def list(index = 0):
        return [elem[index] for elem in TipoIncidencia]

    
@unique
class RegimeTributacao(Enum):
    LUCRO_PRESUMIDO = ("lucro_presumido", "Lucro Presumido")
    LUCRO_REAL = ("lucro_real", "Lucro Real")
    SIMPLES_NACIONAL = ("simples_nacional", "Simples Nacional")
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
      
    def __eq__(self, other):
        if isinstance(other, RegimeTributacao):
            return self.value[0] == other.value[0]
        return False
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:    
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}") 

    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in RegimeTributacao]

@unique
class Finalidade(Enum):
    COMERCIALIZACAO = ("comercializacao", "Comercialização")
    INDUSTRIALIZACAO = ("industrializacao", "Industrialização")
    USO_CONSUMO = ("uso_consumo", "Uso e Consumo")
    IMOBILIZADO = ("imobilizado", "Imobilizado")
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
      
    def __eq__(self, other):
        if isinstance(other, Finalidade):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:    
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")
    
    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in Finalidade]
    
@unique
class TipoCliente(Enum):
    PJ_CONTRIBUINTE = ("pj_contribuinte", "PJ Contribuinte", "pj_contribuinte")
    PJ_NAO_CONTRIBUINTE = ("pj_nao_contribuinte", "PJ Não Contribuinte", "pj_nao_contribuinte")
    CONSUMIDOR_FINAL = ("consumidor_final", "Consumidor Final", "nao_contribuinte")
    DISTRIBUIDOR = ("distribuidor", "Distribuidor", "pj_contribuinte")
    COMERCIO_ATACADISTA = ("comercio_atacadista", "Comércio Atacadista", "pj_contribuinte")
    COMERCIO_VAREJISTA = ("comercio_varejista", "Comércio Varejista", "pj_contribuinte")
    DEPOSITO_FECHADO = ("deposito_fechado", "Depósito Fechado", "pj_contribuinte")
    ARMAZEM_GERAL = ("armazem_geral", "Armazem Geral", "pj_contribuinte")
    INDUSTRIA = ("industria", "Indústria", "pj_contribuinte")
    IMPORTADOR = ("importador", "Importador", "pj_contribuinte")
    GOVERNO = ("governo", "Governo", "nao_contribuinte")    
    TRANSPORTADORA = ("transportadora", "Transportadora", "pj_contribuinte")
    PRESTADOR_SERVICO = ("prestador_servico", "Prestador de Serviços", "pj_nao_contribuinte")
    CONSTRUCAO_CIVIL = ("construcao_civil", "Construção Civil", "pj_nao_contribuinte")    
    PRODUTOR_RURAL = ("produtor_rural", "Produtor Rural", "pj_contribuinte")
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 

    @property
    def codigo(self):
        return self.value[0]
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def classificacao(self):
        return self.value[2]
    
    def __eq__(self, other):
        if isinstance(other, TipoCliente):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:    
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")
    
    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in TipoCliente]
    
@unique    
class NaturezaOperacao(Enum):
    VENDA_PRODUCAO = ("venda_producao", "venda", "saida", "Venda de produção")
    VENDA_MERCADORIA = ("venda_mercadoria", "venda", "saida", "Venda de mercadoria")
    REMESSA_INDUSTRIALIZACAO_SAIDA = ("remessa_industrializacao_saida", "remessa", "saida", "Remessa para industrialização")
    REMESSA_POR_CONTA_ORDEM_SAIDA = ("remessa_por_conta_ordem_saida", "remessa", "saida", "Remsessa por conta de ordem")
    EXPORTACAO = ("exportacao", "venda", "saida", "Exportação")
    TRANSFERENCIA_PRODUCAO_SAIDA = ("transferencia_producao_saida", "transferencia", "saida", "Transferência de produção")
    TRANSFERENCIA_MERCADORIA_SAIDA = ("transferencia_mercadoria_saida", "transferencia", "saida", "Transferência de mercadoria")
    OUTRAS_SAIDAS = ("outras_saidas", "outras", "saidas", "Outras saidas")
    COMPRA_INDUSTRIALIZACAO = ("compra_industrializacao", "compra", "entrada", "Compra para industrialização")
    COMPRA_MERCADORIA = ("compra_mercadoria", "compra", "entrada", "Compra de mercadoria")
    IMPORTACAO = ("importacao", "compra", "entrada", "Importação")
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")

    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in NaturezaOperacao]

    @property
    def tipo_operacao(self):
        return self.value[2]
    
    @property
    def descricao(self):
        return self.value[3]
    
    @property
    def grupo(self):        
        return self.value[1]
    
    @property
    def codigo(self):        
        return self.value[0]
       
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
      
    def __eq__(self, other):
        if isinstance(other, NaturezaOperacao):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False

@unique
class CST_ICMS(Enum):
    CST_00 = ("00", "Tributada integralmente")
    CST_10 = ("10", "Tributada e com cobrança do ICMS por substituição tributária")
    CST_20 = ("20", "Com redução de base de cálculo")
    CST_30 = ("30", "Isenta ou não tributada e com cobrança do ICMS por substituição tributária")
    CST_40 = ("40", "Isenta")
    CST_41 = ("41", "Nao Tributada")
    CST_50 = ("50", "Suspensão")
    CST_51 = ("51", "Diferimento")
    CST_60 = ("60", "ICMS cobrado anteriormente por substituição tributária")
    CST_70 = ("70", "Com redução de base de cálculo e cobrança do ICMS por substituição tributária")
    CST_90 = ("90", "Outros")
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")    
    
    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in CST_ICMS]
    
    def __str__(self):
        return self.value[0]

    def __repr__(self):
        return self.value[0] 
    
    def __eq__(self, other):
        if isinstance(other, CST_ICMS):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]
    
    
@unique
class CST_IPI(Enum):
    CST_00 = ("00", "Entrada com Recuperação de Crédito")   
    CST_01 = ("01", "Entrada Tributada com Aliquota Zero")
    CST_02 = ("02", "Entrada Isenta")
    CST_03 = ("03", "Entrada Nao Tributada")
    CST_04 = ("04", "Entrada Imune")
    CST_05 = ("05", "Entrada com Suspensão")
    CST_49 = ("49", "Outras entradas")
    CST_50 = ("50", "Saida Tributada")
    CST_51 = ("51", "Saida Tributada com Aliquota Zero")
    CST_52 = ("52", "Saida Isenta")
    CST_53 = ("53", "Saida Nao Tributada")
    CST_54 = ("54", "Saida Imune")
    CST_55 = ("55", "Saida com Suspensão")
    CST_99 = ("99", "Outras saidas")
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")
    
    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in CST_IPI]

    def __str__(self):
        return self.value[0]
    
    def __repr__(self):
        return self.value[0] 
    
    def __eq__(self, other):
        if isinstance(other, CST_IPI):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False
    
    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]
    
@unique
class CST_PIS_COFINS(Enum):
    CST_01 = ("01", "Tributada integralmente")
    CST_02 = ("02", "Operação Tributável com Alíquota Diferenciada")
    CST_03 = ("03", "Operação Tributável com Alíquota por Unidade de Medida de Produto")
    CST_04 = ("04", "Operação Tributável Monofásica – Revenda a Alíquota Zero")
    CST_05 = ("05", "Operação Tributável por Substituição Tributária")
    CST_06 = ("06", "Operação Tributável a Alíquota Zero") 
    CST_07 = ("07", "Operação Isenta da Contribuição")
    CST_08 = ("08", "Operação sem incidência da Contribuição")
    CST_09 = ("09", "Operação com suspensão da Contribuição")
    CST_49 = ("49", "Outras Operações de Saída")
    CST_98 = ("98", "Outras Operações de Entrada")
    CST_99 = ("99", "Outras Operações")
    
    @classmethod
    def from_value(cls, valor):
        for elem in cls:
            if elem.value[0] == valor:
                return elem
        raise ValueError(f"{cls.__name__}: invalid value {valor}")

    @staticmethod
    def list(index = 0):
        return [elem.value[index] for elem in CST_PIS_COFINS]
    
    def __str__(self):
        return self.value[0]  
    
    def __repr__(self):
        return self.value[0] 
    
    def __eq__(self, other):
        if isinstance(other, CST_PIS_COFINS):
            return self.value[0] == other.value[0]
        if isinstance(other, str):
            return self.value[0] == other
        return False

    @property
    def descricao(self):
        return self.value[1]
    
    @property
    def codigo(self):
        return self.value[0]

#######################################################################
# Classes de Tributação
#######################################################################
  
@dataclass
class ICMS:
    cst: CST_ICMS
    aliquota: float
    reducao_base_calculo: float
    fcp: float
    fundamento_legal: str    
    
    def __str__(self):
        return f"{self.cst}:{self.aliquota}"

@dataclass
class IPI:
    cst: CST_IPI
    aliquota: float
    descricao_tipi: str
    fundamento_legal: str
    
    def __str__(self):
        return f"{self.cst}:{self.aliquota}"

@dataclass
class PIS_COFINS:
    cst: CST_PIS_COFINS
    aliquota: float
    fundamento_legal: str 
    
    def __str__(self):
        return f"{self.cst}:{self.aliquota}"

