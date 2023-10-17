class Parametres():
    def __init__(self, n_estacions: int, n_bicis: int, llavor: int, n_furgonetes: int, max_bicicletes: int): #, p_min: List[int], p_max: int, c_max: int):
        self.n_estacions = n_estacions
        self.n_bicis = n_bicis
        self.llavor =  llavor
        self.n_furgonetes =  n_furgonetes
        self.max_bicicletes = max_bicicletes
        
    def __repr__(self):
        return f"Parametres(num_estacions={self.n_estacions}, num_bicis={self.n_bicis}, llavor={self.llavor}, num_furgonetes={self.n_furgonetes}"
