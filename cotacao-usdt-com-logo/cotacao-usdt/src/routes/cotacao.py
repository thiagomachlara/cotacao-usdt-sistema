from flask import Blueprint, request, jsonify, render_template
import requests
from src.models.cotacao import db, Cliente, PercentualPadrao

# Blueprint principal para rotas de API
cotacao_bp = Blueprint('cotacao', __name__)

# Blueprint separado para páginas (sem prefixo /api)
pages_bp = Blueprint('pages', __name__)

def obter_cotacao_usdt_brl():
    """Obtém a cotação USDT/BRL da API da Laas"""
    try:
        url = "https://laas.azify.tech/api/v2.0/market/price?pair=USDT_BRL"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar se há dados válidos
            if data.get('data') and data['data'].get('fxRate'):
                return float(data['data']['fxRate'])
            elif data.get('price'):
                return float(data['price'])
            else:
                # API pausada ou sem dados, usar preço simulado
                return 5.50  # Preço simulado para demonstração
        else:
            return 5.50  # Preço simulado em caso de erro
            
    except Exception as e:
        print(f"Erro ao obter cotação: {e}")
        return 5.50  # Preço simulado em caso de erro

@cotacao_bp.route('/cotacao', methods=['GET'])
def get_cotacao():
    """Retorna a cotação atual USDT/BRL"""
    preco_base = obter_cotacao_usdt_brl()
    
    return jsonify({
        'preco_base': preco_base,
        'timestamp': 'now',
        'fonte': 'Laas API'
    })

@cotacao_bp.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna lista de clientes"""
    clientes = Cliente.query.filter_by(ativo=True).all()
    return jsonify([cliente.to_dict() for cliente in clientes])

@cotacao_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    """Cria um novo cliente"""
    data = request.get_json()
    
    if not data or not data.get('nome') or data.get('percentual') is None:
        return jsonify({'erro': 'Nome e percentual são obrigatórios'}), 400
    
    cliente = Cliente(
        nome=data['nome'],
        percentual=float(data['percentual'])
    )
    
    db.session.add(cliente)
    db.session.commit()
    
    return jsonify(cliente.to_dict()), 201

@cotacao_bp.route('/percentuais-padrao', methods=['GET'])
def get_percentuais_padrao():
    """Retorna percentuais padrão disponíveis"""
    percentuais = PercentualPadrao.query.filter_by(ativo=True).all()
    return jsonify([p.to_dict() for p in percentuais])

@cotacao_bp.route('/calcular', methods=['POST'])
def calcular_cotacao():
    """Calcula cotação com markup e volume necessário"""
    data = request.get_json()
    
    if not data:
        return jsonify({'erro': 'Dados não fornecidos'}), 400
    
    percentual = data.get('percentual', 0)
    valor_reais = data.get('valor_reais', 0)
    
    # Obter cotação base
    preco_base = obter_cotacao_usdt_brl()
    
    # Calcular preço com markup para cliente
    multiplicador_cliente = 1 + (percentual / 100)
    preco_cliente = preco_base * multiplicador_cliente
    
    # Nosso custo real é 0.25% acima do spot
    multiplicador_custo = 1 + (0.25 / 100)
    preco_custo = preco_base * multiplicador_custo
    
    # Calcular quantidade de USDT
    usdt_necessario = valor_reais / preco_cliente if preco_cliente > 0 else 0
    
    return jsonify({
        'preco_base': preco_base,
        'preco_cliente': preco_cliente,
        'preco_custo': preco_custo,
        'percentual': percentual,
        'valor_reais': valor_reais,
        'usdt_necessario': usdt_necessario
    })

@pages_bp.route('/billboard', methods=['GET'])
def billboard():
    """Página de billboard público com spread controlável via URL"""
    return render_template('billboard.html')

@cotacao_bp.route('/billboard-cotacao', methods=['GET'])
def get_billboard_cotacao():
    """API para cotação do billboard com spread personalizado"""
    # Obter spread da URL (padrão 1.0 = sem spread)
    spread = request.args.get('spread', '1.0', type=float)
    
    # Validar spread (entre 0.5 e 2.0 para segurança)
    if spread < 0.5 or spread > 2.0:
        spread = 1.0
    
    # Obter cotação base
    preco_base = obter_cotacao_usdt_brl()
    
    # Aplicar spread
    preco_com_spread = preco_base * spread
    
    # Calcular percentual do spread
    percentual_spread = (spread - 1) * 100
    
    return jsonify({
        'preco_base': preco_base,
        'spread': spread,
        'preco_com_spread': preco_com_spread,
        'percentual_spread': percentual_spread
    })

@cotacao_bp.route('/cotacoes-rapidas', methods=['GET'])
def get_cotacoes_rapidas():
    """Retorna cotações 0.5% e 0.65% pré-calculadas"""
    preco_base = obter_cotacao_usdt_brl()
    
    # Calcular preços para clientes
    preco_05 = preco_base * 1.005  # 0.5%
    preco_065 = preco_base * 1.0065  # 0.65%
    
    return jsonify({
        'preco_base': preco_base,
        'cotacao_05': preco_05,
        'cotacao_065': preco_065
    })

# Inicializar dados padrão
def init_dados_padrao():
    """Inicializa dados padrão no banco"""
    # Verificar se já existem percentuais padrão
    if PercentualPadrao.query.count() == 0:
        percentuais_padrao = [
            PercentualPadrao(percentual=0.5, descricao="Básico"),
            PercentualPadrao(percentual=0.65, descricao="Padrão")
        ]
        
        for p in percentuais_padrao:
            db.session.add(p)
        
        db.session.commit()
    
    # Verificar se já existem clientes de exemplo
    if Cliente.query.count() == 0:
        clientes_exemplo = [
            Cliente(nome="Cliente Feitosa", percentual=0.65),
            Cliente(nome="Brasil OTC", percentual=0.5)
        ]
        
        for c in clientes_exemplo:
            db.session.add(c)
        
        db.session.commit()

