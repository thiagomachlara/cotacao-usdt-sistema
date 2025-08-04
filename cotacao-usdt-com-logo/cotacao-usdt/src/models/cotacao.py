from src.models.user import db

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    percentual = db.Column(db.Float, nullable=False)  # Percentual de markup (ex: 0.65 para 0.65%)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Cliente {self.nome} - {self.percentual}%>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'percentual': self.percentual,
            'ativo': self.ativo
        }

class PercentualPadrao(db.Model):
    __tablename__ = 'percentuais_padrao'
    
    id = db.Column(db.Integer, primary_key=True)
    percentual = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<PercentualPadrao {self.percentual}% - {self.descricao}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'percentual': self.percentual,
            'descricao': self.descricao,
            'ativo': self.ativo
        }

