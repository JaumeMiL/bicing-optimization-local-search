class Parametres():
    def __init__(self, n_estacions: int, n_bicis: int, llavor: int, num_furgonetes: int, max_bicicletes: int):
        self.n_estacions = n_estacions
        self.n_bicis = n_bicis
        self.llavor =  llavor
        self.num_furgonetes =  num_furgonetes 
        self.max_bicicletes = max_bicicletes
        
    def __repr__(self):
        return f"Parametres(num_estacions={self.n_estacions}, num_bicis={self.n_bicis}, llavor={self.llavor}, num_furgonetes={self.num_furgonetes}"