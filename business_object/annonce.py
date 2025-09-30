
class Annonce():
    def __init__(self,id_annonce,city,url_image,source,price,kind,surface,room, agency, description,title):
        self.id_annonce = id_annonce
        self.city = city
        self.url_image = url_image
        self.source = source 
        self.price = price 
        self.kind = kind 
        self.surface = surface
        self.room = room
        self.agency = agency
        self.description=description
        self.title=title

    def __str__(self) -> str:
        if self.agency != 'Indisponible' :
            return('Magnifique {} de {}m² à {} avec {} pièce.s à seulement {}€ à l\'agence {}.'.format(self.kind, self.surface, self.city, self.room, self.price, self.agency))
        else:
            return('Magnifique {} de {}m² à {} avec {} pièce.s à seulement {}€.'.format(self.kind, self.surface, self.city, self.room, self.price))
