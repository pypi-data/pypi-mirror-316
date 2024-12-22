class ContextoFiscalRegistry:
    _registry = {}

    @classmethod
    def registrar(cls, nome, classe):
        """Registra uma implementação no registro."""
        cls._registry[nome] = classe

    @classmethod
    def obter_classe(cls, nome):
        """Obtém uma classe registrada pelo nome."""
        return cls._registry.get(nome)

    @classmethod
    def listar_implementacoes(cls):
        """Lista todas as implementações disponíveis."""
        return list(cls._registry.keys())
    

# um decorador para que as implementações se registrem automaticamente.
def registrar_contexto(nome):
    def decorador(classe):
        ContextoFiscalRegistry.registrar(nome, classe)
        return classe
    return decorador