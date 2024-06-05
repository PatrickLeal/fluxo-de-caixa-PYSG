class Movimentacao():
    def __init__(self,DATA_txt: str, ID_TIPO_num: int, ID_CATEGORIA_num: int, OBSERVACAO_txt: str, VALOR_num: float,) -> None:
        self.DATA_txt = DATA_txt
        self.ID_TIPO_num = ID_TIPO_num
        self.ID_CATEGORIA_num = ID_CATEGORIA_num
        self.OBSERVACAO_txt = OBSERVACAO_txt
        self.VALOR_num = VALOR_num