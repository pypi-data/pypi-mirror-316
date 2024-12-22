import json
from mapafiscal.common import *
from mapafiscal.contexto import ContextoFiscal, ContextoFiscalException
from mapafiscal.contexto import Aliquota, ExcecaoFiscal, PautaFiscal, CenarioIncidencia
from mapafiscal.contexto.factory import registrar_contexto
from pathlib import Path

path = Path(__file__).parent
    
    
@registrar_contexto("json")    
class JSONContexto(ContextoFiscal):
    encoding = 'utf-8'

    def __init__(self, uf_origem: str, 
                 regime_tributario: RegimeTributacao, 
                 perfil: PerfilContribuinte, 
                 contexto_file: str = None):
        """
        Inicializa o JSONContexto e carrega os dados padrão.
        """
        super().__init__(uf_origem, regime_tributario, perfil)
        self._aliquotas = []
        self._excecoes = []
        self._pautas = []
        self._cenarios = []

        # Carregar arquivos iniciais usando os métodos otimizados
        self._load_dados(f"{path}/etc/aliquotas.json", "aliquotas", Aliquota, self._aliquotas)
        self._load_dados(f"{path}/etc/excecoes_fiscais.json", "excecoes_fiscais", ExcecaoFiscal, self._excecoes)
        self._load_dados(f"{path}/etc/pautas_fiscais.json", "pautas_fiscais", PautaFiscal, self._pautas)
        self._load_dados(f"{path}/etc/cenarios_incidencias.json", "cenarios_incidencias", CenarioIncidencia, self._cenarios)
        
        # Carregar arquivos adicionais, se fornecidos
        if contexto_file:
            self.add_aliquotas(contexto_file)
            self.add_excecoes_fiscais(contexto_file)
            self.add_pautas_fiscais(contexto_file)
            self.add_cenarios_incidencias(contexto_file)
            
        # Carregar tabela do IPI
        self._load_tipi(f"{path}/etc/tabela_ipi_hierarquica.json")

    def _load_dados(self, json_file: str, chave: str, classe, lista_destino: list):
        """
        Carrega dados de um arquivo JSON e adiciona instâncias à lista destino.

        Args:
            json_file (str): Caminho do arquivo JSON.
            chave (str): Chave principal do JSON.
            classe: Classe de destino para criação das instâncias.
            lista_destino (list): Lista onde os dados serão armazenados.
        """
        try:
            with open(json_file, 'r', encoding=self.encoding) as arquivo:
                data = json.load(arquivo)
                lista_destino.extend(
                    classe(**item) for item in data.get(chave, [])
                )
        except FileNotFoundError:
            raise ContextoFiscalException(f"Erro: O arquivo {json_file} não foi encontrado.")
        except json.JSONDecodeError:
            raise ContextoFiscalException(f"Erro: O arquivo {json_file} não está em um formato JSON válido.")
        except Exception as e:
            raise ContextoFiscalException(f"Erro inesperado ao carregar {json_file}: {e}")

    def add_aliquotas(self, json_file: str):
        """Carrega e mescla novas alíquotas a partir de um arquivo JSON adicional."""
        self._load_dados(json_file, "aliquotas", Aliquota, self._aliquotas)
        
    def add_excecoes_fiscais(self, json_file: str):
        """Carrega e mescla novas exceções fiscais a partir de um arquivo JSON adicional."""
        self._load_dados(json_file, "excecoes_fiscais", ExcecaoFiscal, self._excecoes)
        
    def add_pautas_fiscais(self, json_file: str):
        """Carrega e mescla novas pautas fiscais a partir de um arquivo JSON adicional."""
        self._load_dados(json_file, "pautas_fiscais", PautaFiscal, self._pautas)

    def add_cenarios_incidencias(self, json_file: str):
        """Carrega e mescla novos cenários de incidência a partir de um arquivo JSON adicional."""
        self._load_dados(json_file, "cenarios_incidencias", CenarioIncidencia,self._cenarios)

        
    def list_all_aliquotas(self):
        return self._aliquotas
    
    def list_all_cenarios(self):
        return self._cenarios
    
    def list_all_excecoes(self):
        return self._excecoes
    
    def list_all_pautas(self):
        return self._pautas
    
    
    def _load_tipi(self, json_file: str, encoding: str = 'utf-8'):
        with open(json_file, 'r', encoding=encoding) as arquivo:
            data = json.load(arquivo)
            
            for item in data:
                aliq_ipi = item.get('aliquota', None)
                
                if not aliq_ipi is None:
                    self._aliquotas.append(
                        Aliquota(
                            tributo="IPI",
                            uf="BR",
                            aliquota=float(aliq_ipi) if aliq_ipi != "NT" else 0.0,
                            descricao_tipi=item.get('descricao', ''),
                            ncm=item.get('ncm')
                    ))
            

                
            