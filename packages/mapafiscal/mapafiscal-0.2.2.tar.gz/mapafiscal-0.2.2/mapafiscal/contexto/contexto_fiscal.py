from abc import abstractmethod, ABC
from typing import List
from mapafiscal.contexto.model import Aliquota, ExcecaoFiscal, PautaFiscal, CenarioIncidencia
from mapafiscal.model import RegimeTributacao, PerfilContribuinte
from mapafiscal.common import NaturezaOperacao, TipoCliente, Finalidade

class ContextoFiscalException(Exception):
    """Base class for exceptions in this module."""
    pass   

class ContextoFiscal(ABC):
    
    """Classe base que contém contexto de dados tributários e fiscais."""

    @abstractmethod
    def list_all_aliquotas(self) -> List[Aliquota]:
        pass

    @abstractmethod
    def list_all_excecoes(self) -> List[ExcecaoFiscal]:
        pass

    @abstractmethod
    def list_all_pautas(self) -> List[PautaFiscal]:
        pass

    @abstractmethod
    def list_all_cenarios(self) -> List[CenarioIncidencia]:
        pass

    def __init__(self, uf_origem: str, regime_tributacao: RegimeTributacao, perfil_contribuinte: PerfilContribuinte):
        self._uf_origem = uf_origem
        self._regime_tributacao = regime_tributacao
        self._perfil_contribuinte = perfil_contribuinte
    
    @property
    def uf_origem(self): 
        return self._uf_origem
    
    @property
    def regime_tributacao(self) -> RegimeTributacao: 
        return self._regime_tributacao
    
    @property
    def perfil_contribuinte(self) -> PerfilContribuinte: 
        return self._perfil_contribuinte
    
    def list_aliquota_by_tributo(self, tributo: str):
        return [aliquota for aliquota in self.list_all_aliquotas() if aliquota.tributo == tributo]
    
    def list_excecoes_by_tributo(self, tributo: str):
        return [excecao for excecao in self.list_all_excecoes() if excecao.tributo == tributo]
    
    def list_pauta_by_cest(self, cest: str):
        return [pauta for pauta in self.list_all_pautas() if pauta.cest == cest]
    
    def list_cenario_by_natureza(self, natureza_operacao: NaturezaOperacao):
        return [operacao for operacao in self.list_all_cenarios() if operacao.natureza_operacao == natureza_operacao.codigo]

         
    def find_excecao_fiscal(self, ncm: str, tributo: str, uf: str = '') -> ExcecaoFiscal:
        """
        Procura uma exceção fiscal para um determinado NCM, tributo ou UF.
        Dependendo do tributo, a determinação da aliquota depende do NCM ou da UF.
        
        Args:
            ncm (str): NCM da exceção fiscal
            tributo (str): Tributo da exceção fiscal
            uf (str): UF da exceção fiscal
        
        Returns:
            ExcecaoFiscalConfig
        """
        excecoes = self.list_excecoes_by_tributo(tributo=tributo)
        if uf == '':
            for excecao in excecoes:
                if ncm == excecao.ncm:
                    return excecao
        else:    
            for excecao in excecoes:
                if uf.upper() == excecao.uf and ncm == excecao.ncm:
                    return excecao
        return None
    
    def find_cenario_incidencia(self, 
                                natureza_operacao: NaturezaOperacao, 
                                tipo_cliente: TipoCliente,
                                finalidade: Finalidade) -> CenarioIncidencia:        
        """
        Procura um cenario para um determinada Natureza de Operação, Tipo de Cliente e Finalidade.
        
        Args:
            natureza_operacao (NaturezaOperacao): Natureza de Operação
            tipo_cliente (TipoCliente): Tipo de Cliente
            finalidade (Finalidade): Finalidade
        
        Returns:
            CenarioConfig
        """        
        
        for cenario in self.list_all_cenarios():
            if cenario.natureza_operacao == natureza_operacao and \
                cenario.finalidade == finalidade and cenario.tipo_cliente == tipo_cliente:
                return cenario
        
        raise ContextoFiscalException(f"Configuração para operação não encontrada para os parâmetros informados:" 
                                      f"natureza_operacao={natureza_operacao}, " 
                                      f"tipo_cliente={tipo_cliente}, "
                                      f"finalidade={finalidade}")
  
    def find_pauta_fiscal(self, cest: str, uf_destino: str) -> PautaFiscal:     
        """
        Obtém a Pauta ST para um determinado CEST e UF destino.
        
        Args:
            cest (str): CEST da pauta
            uf_destino (str): UF destino da pauta
        
        Returns:
            PautaConfig
        """        
        if cest == '': 
            raise ContextoFiscalException("CEST deve ser informado")
        
        if uf_destino == '':
            raise ContextoFiscalException("UF destino deve ser informado")
        
        for pauta in self.list_pauta_by_cest(cest=cest):
            if pauta.uf_destino == uf_destino:
                return pauta
        return None

    def find_aliquota(self, tributo: str, uf: str = "BR", ncm: str = "") -> Aliquota:
        """
        Obtém a aliquota para um determinado tributo de acordo com o NCM ou UF.
        
        Args:
            tributo (str): Tributo
            uf (str): UF
            ncm (str): NCM
        
        Returns:
            Aliquota
        """
        
        match(tributo):
            case "ICMS":
                if uf == "BR":
                    raise ContextoFiscalException("UF deve ser informada")
                
                for aliquota_icms in self.list_aliquota_by_tributo(tributo="ICMS"):
                    if aliquota_icms.uf == uf:
                        return aliquota_icms
            
            case "IPI":
                if ncm == "":
                    raise ContextoFiscalException("NCM deve ser informado")
                
                for aliquota in self.list_aliquota_by_tributo(tributo=tributo):
                    if aliquota.ncm == ncm:
                        return aliquota
                
            case "PIS" | "COFINS":
            
                if ncm == "": 
                    raise ContextoFiscalException("NCM deve ser informado")

                if self.regime_tributacao == 'Lucro Real':            
                    return Aliquota(tributo=tributo, 
                                    ncm=ncm, 
                                    uf=uf,
                                    aliquota=1.65 if tributo == "PIS" else 7.6, 
                                    fcp=0.0, 
                                    reducao_base_calculo=0.0,
                                    descricao_tipi="")

                elif self.regime_tributacao == 'Lucro Presumido':            
                    return Aliquota(tributo=tributo, 
                                    ncm=ncm, 
                                    uf=uf,
                                    aliquota=0.65 if tributo == "PIS" else 3.0, 
                                    fcp=0.0, 
                                    reducao_base_calculo=0.0,
                                    descricao_tipi="")
            
            case _:
                # Busca a aliquota para o tributo informado, caso ela exista, retorna a primeira ocorrencia encontrada
                aliquotas = self.list_aliquota_by_tributo(tributo=tributo)
                if len(aliquotas) > 0:
                    return aliquotas[0] 
        
        # Caso nenhuma aliquota seja encontrada, retorna a aliquota zero
        return Aliquota(tributo=tributo, 
                        ncm=ncm, 
                        uf=uf,
                        aliquota=0.0,
                        fcp=0.0,                                             
                        descricao_tipi="")

