from mapafiscal.contexto.factory.contexto_registry import ContextoFiscalRegistry
from mapafiscal.common import RegimeTributacao, PerfilContribuinte
from mapafiscal.contexto.contexto_fiscal import ContextoFiscal


class ContextoFiscalFactory:
    @staticmethod
    def criar_contexto(nome: str, 
                       uf_origem: str, 
                       regime_tributacao: RegimeTributacao, 
                       perfil_empresa: PerfilContribuinte, 
                       **kwargs) -> ContextoFiscal:
        """
        Cria uma instância de ContextoFiscal com base no nome registrado.
        """
        classe = ContextoFiscalRegistry.obter_classe(nome)
        if not classe:
            raise ValueError(f"ContextoFiscal '{nome}' não está registrado.")
        return classe(uf_origem, regime_tributacao, perfil_empresa, **kwargs)
