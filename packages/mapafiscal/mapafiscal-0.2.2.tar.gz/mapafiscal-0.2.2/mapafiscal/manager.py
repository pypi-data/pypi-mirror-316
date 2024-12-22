import json
from mapafiscal.builder import MapaFiscalBuilder
from mapafiscal.common import NaturezaOperacao, TipoCliente, Finalidade
from mapafiscal.common import RegimeTributacao, PerfilContribuinte
from mapafiscal.contexto.factory import ContextoFiscalFactory
from mapafiscal.contexto import JSONContexto


def build_cenario(cenario_file: str, encoding: str = 'utf-8'):
    """Função principal para construção do mapa fiscal a partir de um arquivo de configuração."""
    
    with open(cenario_file, encoding=encoding) as file:
        
            config = json.load(file)
            
            cliente= config["cliente"]
            produtos = config.get("produtos", [])
            cenarios = config.get("cenarios", [])
            uf_origem = config["uf_origem"]
            regime_tributacao = RegimeTributacao.from_value(config["regime_tributacao"])
            perfil_empresa = PerfilContribuinte.from_value(config["perfil_empresa"])
        
    # Criando contexto fiscal
    contexto = ContextoFiscalFactory.criar_contexto(nome="json",
                                                    uf_origem=uf_origem, 
                                                    regime_tributacao=regime_tributacao, 
                                                    perfil_empresa=perfil_empresa,
                                                    contexto_file=cenario_file)
    
    # Construindo mapa fiscal
    mapa_builder = MapaFiscalBuilder(cliente, contexto)
    
    for produto in produtos:    
        classe_fiscal = mapa_builder.build_classe_fiscal(codigo=produto.get("codigo"), 
                                                         ncm=produto.get("ncm"), 
                                                         descricao=produto.get("descricao", ""), 
                                                         origem=produto.get("origem", 0),
                                                         cest=produto.get("cest", ""),
                                                         segmento=produto.get("segmento", ""),
                                                         fabricante_equiparado=produto.get("fabricante_ou_equiparado", False))
        

        mapa_builder.build_classes_st(classe_fiscal=classe_fiscal)
        
        for cenario in cenarios:
        
            mapa_builder.build_cenarios(grupo=cenario.get("grupo", "padrao"),
                                        natureza_operacao=NaturezaOperacao.from_value(cenario["natureza_operacao"]),
                                        tipo_cliente=TipoCliente.from_value(cenario["tipo_cliente"]),
                                        finalidade=Finalidade.from_value(cenario["finalidade"]),
                                        classe_fiscal=classe_fiscal,
                                        uf_list=cenario.get("uf_list"))
            
            mapa_builder.build_operacoes(grupo=cenario.get("grupo", "padrao"), classe_fiscal=classe_fiscal)     
                   
    return mapa_builder.build(f"Mapa Fiscal - {cliente}")    

