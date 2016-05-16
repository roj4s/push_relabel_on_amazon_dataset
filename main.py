# -*- coding: utf8 -*-
import math
import random
from collections import OrderedDict
import time

class Grafo:
	
	def get_vertices(self):
		'''
		Retorna todos os vertices neste grafo
		:return: list
		'''
		val_vert = self.vertices.values()
		return list(val_vert)

	def get_arestas(self):
		'''
		Retorna todas as arestas neste grafo
		:return: list
		'''
		return list(self.arestas)

	def __init__(self):
		self.arestas = []
		self.vertices = OrderedDict()

	def nova_aresta(self, s, d, data = None):
		'''
		Adiciona um nova aresta ao grafo
		:param s:
		:param d:
		:param data:
		:type s: str
		:type d: str
		:type data: dict
		:return:
		'''
		origen = self.buscar_vertice(s)
		destino = self.buscar_vertice(d)
		if origen is None or destino is None:
			origen, destino = self.buscar_vertice_ou_lista_vertices([s, d])
		aresta = Aresta(origen, destino, data)
		self.arestas.append(aresta)
		origen.nova_aresta_de_saida(aresta)
		destino.nova_aresta_entrando(aresta)
		return aresta

	def novo_vertice(self, vertice):
		'''
		Adiciona um novo vertice 'a lista de vertices do grafo
		:param vertice: Vertice a ser adicionado
		:type vertice: Vertice
		:return:
		'''
		self.vertices[vertice.nome] = vertice

	def put_many_vertices(self, lista_vertices):
		'''
		Adiciona varios vertices ao grafo
		:param lista_vertices: Lista que contem os vertices que vai se adicionadar
		:return: list
		'''
		lista_final = []
		for key in lista_vertices:
			lista_final.append(self.novo_vertice(Vertice(key)))
		return lista_final

	def buscar_vertice(self, _key):
		'''
		Procurar um n'o dada sua chave o localizador
		:param _key: Id do n'o
		:type _key: str
		:return: Vertice
		'''
		found_node = self.vertices.get(_key)
		if found_node is not None:
			return found_node
		return None

	def aresta_invertida(self, aresta_a_invertir):
		'''
		Dada uma aresta retorna uma con origen = destino e destino = origen
		:param aresta_a_invertir: aresta a ser virada
		:type aresta_a_invertir: Aresta
		:return: Edge
		'''
		return aresta_a_invertir.no_destino().aresta_ate_no(aresta_a_invertir.no_origem())

	def buscar_vertice_ou_lista_vertices(self, lista_vertices):
		'''
		Dado um vertice ou lista de vertices retorna aqueles que estao no grafo
		:param lista_vertices: Um vertice ou uma lista de vertices
		:type lista_vertices: list
		:return: list
		'''
		_list = []
		for obj in lista_vertices:
			if obj in self.get_vertices():
				_list.append(obj)
			else:
				_list.append(self.vertices.get(obj))
		if len(_list) == 1:
			return _list[0]
		return _list

	def existe_aresta_invertida(self, aresta):
		'''
		Retorna verdadeiro se a aresta tem uma invertida no grafo
		:param aresta:
		:type aresta: Aresta
		:return: bool
		'''
		return self.aresta_invertida(aresta) is not None

class Vertice:

	'''
	Esta classe representa um vertice de um grafo
	com os atributos exeso e altura para ser utilizados no
	algoritmo Push_relabel utilizado neste trabalho.
	'''

	def __init__(self, nome, exesso = 0, altura =0, data = None):
		'''
		Nos do grafo
		:param nome: Rotulo do vertice
		:param exesso: Reresenta el fluxo em exesso que contem esse n'o
		:param altura: Reresenta la altura que esta esse n'o
		:param data: Atributos adicionais
		:type nome: str
		:type exesso: int
		:type altura: int
		:type data: dict
		:return: Vertice
		'''

		self.nome = nome
		self.exesso = exesso
		self.altura = altura
		self.arestas_vao_fora = OrderedDict()
		self.arestas_que_entram = OrderedDict()
		self.fluxo = 0
		self.capacidade = 0
		if data is not None:
			for key, value in data.items():
				setattr(self, key, value)

	def nova_aresta_de_saida(self, aresta):
		'''
		Adiciona uma nova aresta que sai nesste n'o
		:param aresta: Aresta que vai ser adicionada
		:type aresta: Aresta
		:return:
		'''
		self.arestas_vao_fora[aresta.no_destino()] = aresta

	def nova_aresta_entrando(self, aresta):
		'''
		Adiciona uma nova aresta que entra neste n'o
		:param aresta: Aresta que vai ser adicionada
		:type aresta: Aresta
		:return:
		'''
		self.arestas_que_entram[aresta.no_origem()] = aresta

	def get_nome(self):
		'''
		Retorna o identificador ou chave desta aresta
		:return: str
		'''
		return self.nome

	def get_exesso(self):
		'''
		Valor de la variable exesso
		:return: int
		'''
		return self.exesso

	def get_arestas_saindo(self):
		'''
		Retorna uma lista que contem as arestas que vao fora neste vertice
		:return: list
		'''
		return list(self.arestas_vao_fora.values())

	def aresta_ate_no(self, destino):
		'''
		Se existe retorna aquela aresta que une este n'o com um no destino dado
		:param destino: N'o destino
		:type destino: Vertice
		:return: Aresta
		'''
		return self.arestas_vao_fora.get(destino)

	def aresta_desde_no(self, origem):
		'''
		Se existe retorna aquela aresta a qual este n'o 'e destino e origem 'e um n'o dado
		:param origem: N'o dado como origem
		:type origem: Vertice
		:return: Aresta
		'''
		aresta = self.arestas_que_entram.get(origem)
		return aresta

class Aresta:
	'''
	Esta classe representa uma aresta de um grafo
	'''

	def __init__(self, verticeA, verticeB, other_attribs = None):
		'''
		Union de dos vertices
		:param verticeA: N'o origen da aresta
		:param verticeB: N'o destino da aresta
		:param capacidade: Quanto fluxo admite essa aresta
		:param fluxo: Fluxo da aresta
		:param other_attribs: Atributos adicionais
		:type verticeA: Vertice
		:type verticeB: Vertice
		:type capacidade: int
		:type fluxo: int
		:type other_attribs: dict
		:return: Aresta
		'''
		self.verticeA = verticeA
		self.verticeB = verticeB
		if other_attribs is not None:
			for k, v in other_attribs.items():
				setattr(self, k, v)

	def no_origem(self):
		'''
		Retorna o n'o inicial ou n'o origem
		:return: Vertice
		'''
		return self.verticeA

	def no_destino(self):
		'''
		Retorna o n'o final ou n'o destino
		:return:Vertice
		'''
		return self.verticeB

	def get_vertices(self):
		'''
		Retorna uma tupla com os vertices os quais essa aresta une
		:return:
		'''
		return [self.verticeA, self.verticeB]

class Push_Relabel:
	'''
	Implementaçao generica do algoritmo push-relabel baseado no libro
	Introduction to Algorithms de Thomas H. Cormen 736 - 759
	'''

	def __init__(self, grafo):
		'''
		Neste metodo se executa el algoritmo para el grafo passado como parametro
		:param grafo:
		:type grafo: Grafo
		:return:
		'''

		self.grafo = grafo

		for vert in self.grafo.get_vertices():
			vert.altura = 0
			vert.exesso = 0

		for aresta in self.grafo.get_arestas():
			aresta.fluxo = 0
			if not self.grafo.existe_aresta_invertida(aresta):
				self.grafo.nova_aresta(aresta.no_destino(), aresta.no_origem(), {"fluxo":0, "capacidade":0})
		
		s = self.grafo.buscar_vertice("s")
		s.altura = len(self.grafo.get_vertices())

		for aresta in s.get_arestas_saindo():
			aresta.fluxo = aresta.capacidade
			aresta.no_destino().exesso = aresta.fluxo
			aresta.no_destino().aresta_ate_no(s).fluxo = -aresta.capacidade

		while self.ainda_tem_algum_no_ativo():
			no = self.procurar_no_ativo()
			for aresta in no.get_arestas_saindo():
				vizinho = aresta.no_destino()
				if no.altura == vizinho.altura + 1 or aresta.capacidade != aresta.fluxo:
					self.push(aresta)
					if no.exesso == 0:
						break
				else:
					self.relabel(no)

		verts = self.grafo.vertices.values()
		print "Pj' encontrado: " + str(verts[len(verts)-1].exesso)

	def ainda_tem_algum_no_ativo(self):
		'''
		Retorna verdadeiro se ainda existem n'os ativos
		:return: bool
		'''
		if not self.procurar_no_ativo() is None:
			return True
		return False

	def procurar_no_ativo(self):
		'''
		Procura por algum n'o ativo o seja procura algum n'o cujo fluxo seja maior que 0 e nao seja s ou t
		:return: Vertice
		'''
		for no in self.grafo.get_vertices():
			if not no is self.grafo.buscar_vertice("t") and not no is self.grafo.buscar_vertice("s") and no.exesso > 0:
				return no
		return None

	def push(self, aresta):
		'''
		Dado que a aresta admite mais fluxo faca uma operacao push
		:type aresta: Aresta
		'''
		capacidade_residual = aresta.capacidade - aresta.fluxo
		delta = min(capacidade_residual, aresta.no_origem().exesso)
		aresta.fluxo += delta
		aresta.no_origem().aresta_desde_no(aresta.no_destino()).fluxo -= delta
		aresta.no_destino().exesso += delta
		aresta.no_origem().exesso -= delta

	def relabel(self, no):
		"""
    	Relabel esse n'o adjustando sua altura para la minima de sus vizinhos mais um.
    	:type no: Vertice
    	"""

		minimo = None
		for aresta in no.get_arestas_saindo():
			if aresta.fluxo == aresta.capacidade:
				continue
			if minimo is None or aresta.no_destino().altura < minimo:
				minimo = aresta.no_destino().altura
		no.altura = minimo + 1

class Main:

	def __init__(self):
		pass

	def get_percentagem_dos_clientes(self, porcentagem, lista_clientes):
		'''
		Utilizado para excluir um porcentagem dos clientes da base
		:param porcentagem:
		:param lista_clientes:
		:type porcentagem: int
		:type lista_clientes: dict
		:return:
		'''

		print "Tirando " + str(porcentagem) + "% do total dos clientes"

		# # Esses clientes foram considerados outliers
		lista_clientes.pop('A3UN6WX5RRO2AG')
		lista_clientes.pop('ATVPDKIKX0DER')

		upper_bound = len(lista_clientes) - int(len(lista_clientes) * porcentagem / 100)
		_keys = lista_clientes.keys()
		for i in range(0, upper_bound):
			lista_clientes.pop(_keys[i])
		return lista_clientes

	def obter_costumers_da_base(self, base_addr):
		'''
		Parser para leer o arquivo e obter reviews cliente -> produto
		:param base_addr: Endereco da base de dados
		:type base_addr: str
		:return: dict
		'''

		_file = open(base_addr, 'r')

		dict_produtos_aux = {}
		dict_clientes = {}
		lendo = _file.readline()
		while(lendo):
			if "Id:" in lendo:
				id_produto = lendo.split()[1]
			elif "cutomer:" in lendo:
				if lendo.split()[2] in dict_clientes:
					if id_produto not in dict_clientes[lendo.split()[2]]:
						dict_produtos_aux = dict_clientes[lendo.split()[2]]
						dict_produtos_aux[id_produto] = 1
						dict_clientes[lendo.split()[2]] = dict_produtos_aux
				else:
					dict_produtos_aux[id_produto] = 1
					dict_clientes[lendo.split()[2]] = dict_produtos_aux

			dict_produtos_aux = {}
			lendo = _file.readline()
		_file.close()
		return dict_clientes

	def obter_produtos(self, dict_clientes):
		'''
		Dado a estructura clientes {clienteK:{Producto1 ... ProductoM}} atualiza quantidade de reviews de cada produto
		:param dict_clientes:
		:return: dict
		'''
		ids_clients = dict_clientes.keys()
		dict_produtos = {}

		for _id in ids_clients:
			for id_product in dict_clientes[_id].keys():
				if id_product in dict_produtos:
					dict_produtos[id_product] = dict_produtos[id_product] + 1
				else:
					dict_produtos[id_product] = 1
		return dict_produtos

	def criar_grafo(self, dict_clientes, dict_produtos):
		'''
		Metodo para criar o grafo bipartido con s => clientes => produtos => t
		:param dict_clientes:
		:param dict_produtos:
		:type dict_clientes: dict
		:type dict_produtos: dict
		:return: Grafo
		'''

		grafo = Grafo()
		vertices = ["s"] + dict_clientes.keys() + dict_produtos.keys() + ["t"]
		grafo.put_many_vertices(vertices)
		total_rev_40p_clients = 0
		total_rev_clients = 0
		percentagem_pj = float(input("Escreva o porcentagem para Pj: "))
		for id_cliente in (dict_clientes.keys()):
			quantidade_clientes40perc = int(len(dict_clientes[id_cliente]) * 0.4)
			grafo.nova_aresta("s", id_cliente, {"capacidade" : quantidade_clientes40perc})
			total_rev_clients += int(len(dict_clientes[id_cliente]))
			total_rev_40p_clients += quantidade_clientes40perc

		print 'Quantidade de reviews dos clientes: ' + str(total_rev_clients)

		#arestas intermedias
		for id_cliente in (dict_clientes.keys()):
			for id_producto in dict_clientes[id_cliente].keys():
				grafo.nova_aresta(id_cliente, id_producto, {"capacidade": 1})

		total_rev_produtos = 0
		pj_linha = 0
		for id_produto in dict_produtos.keys():
			quantidade_tirando_perct = math.ceil(dict_produtos[id_produto]*float(percentagem_pj/100))
			grafo.nova_aresta(id_produto, "t", {"capacidade": int(quantidade_tirando_perct)})
			total_rev_produtos += int(dict_produtos[id_produto])
			pj_linha += quantidade_tirando_perct

		print "Total de reviews dos produtos - Pj: " + unicode(total_rev_produtos)
		print "40% dos reviews dos clientes - Ci': " + unicode(total_rev_40p_clients)
		print unicode(percentagem_pj) + "% de reviews do Produto - Pj': " + unicode(int(pj_linha))

		return grafo

def main():
	print "~~~0~~~~1~0~0~1~~~0~~1~~~~~~~1~~~~0~~~~1~~~0~~~~0~0~~~~~~~~~0~~~~~1~~~~~~~~"
	print "                                           "
	print "                          PPGI - ICOMP - UFAM                              "
	print "                    Projeto e analise de algoritmos     "
	print "           Trabalho Pratico # 2: Fluxo maximo em grafos bipartidos. "
	print "                                                             "
	print "                       Ing. Luis Miguel Rojas Aguilera          "
	print "                                           "
	print "~0~~~~1~~~0~~~1~0~0~~~~~~~0~~0~~~~1~~~~1~0~0~~0~~~~1~~~~1~0~~~~~~~~~1~~~~~~~"

	nome_base = unicode(raw_input("Porfavor insira o nome da base (endereço se não estiver na misma pasta): "))

	dict_clientes = Main().obter_costumers_da_base(nome_base)

	print "Essa base tem ", len(dict_clientes.keys()), " clientes"
	porcentagem = float(raw_input("Digite a porcentagem de clientes a utilizar: "))

	print ".................. Criando grafo .................."
	dict_clientes = Main().get_percentagem_dos_clientes(porcentagem, dict_clientes)
	dict_produtos = Main().obter_produtos(dict_clientes)
	print "Total de clientes:  " + str(len(dict_clientes))
	print "Total de produtos: " + str(len(dict_produtos))
	grafo = Main().criar_grafo(dict_clientes, dict_produtos)
	print "............. Executando o fluxo maximo ..........."

	start_time_stamp = time.time()
	Push_Relabel(grafo)
	end_time_stamp = time.time()
	difference_time = end_time_stamp - start_time_stamp
	print "Concluido, tempo total: ", difference_time

if __name__ == "__main__":
	main()
