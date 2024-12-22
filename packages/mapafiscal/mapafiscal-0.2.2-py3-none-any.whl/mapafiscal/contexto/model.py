from mapafiscal.common import *


@dataclass
class Aliquota:
    tributo: str    
    uf: str
    aliquota: float
    fcp: float = 0.0
    ncm: str = ''
    descricao_tipi: str = ''

    def __str__(self):
        return f"Tributo: {self.tributo}, Aliquota: {self.aliquota}"
 
@dataclass
class ExcecaoFiscal:
    tributo: str
    uf: str
    ncm: str    
    aliquota: float
    fcp: float
    reducao_base_calculo: float
    cst: str
    descricao_tipi: str
    fundamento_legal: str
    
    def __str__(self):
        return f"Tributo: {self.tributo}, Aliquota: {self.aliquota}, Fundamento Legal: {self.fundamento_legal}"

@dataclass
class PautaFiscal:
    uf_origem: str
    uf_destino: str
    cest: str
    descricao_cest: str
    segmento: str
    mva_original: float
    fundamento_legal: str
    
    def __str__(self):
        return f"UF Origem: {self.uf_origem}, "\
            f"UF Destino: {self.uf_destino}, "\
            f"CEST: {self.cest}, "\
            f"Segmento: {self.segmento}, "\
            f"MVA original: {self.mva_original}, "\
            f"Fundamento Legal: {self.fundamento_legal}"
            
   
@dataclass
class CenarioIncidencia:
    codigo: str
    natureza_operacao: NaturezaOperacao
    finalidade: Finalidade
    tipo_cliente: TipoCliente    
    cfop_interno: str
    cfop_interno_st: str
    cfop_interno_devolucao: str
    cfop_interno_devolucao_st: str
    cfop_interestadual: str
    cfop_interestadual_st: str
    cfop_interestadual_devolucao: str
    cfop_interestadual_devolucao_st: str
    incidencia_icms: TipoIncidencia
    incidencia_icms_st: TipoIncidencia
    incidencia_ipi: TipoIncidencia
    incidencia_pis_cofins: TipoIncidencia
    fundamento_legal: str         
    
    def __str__(self):
        return f"Código: {self.codigo}, "\
            f"Natureza Operação: {self.natureza_operacao}, "\
            f"Finalidade: {self.finalidade}, "\
            f"Tipo Cliente: {self.tipo_cliente}"