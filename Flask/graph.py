import networkx as nx
import matplotlib.pyplot as plt
from Flask.methodsMongoDb import MethodsCollection
from flask import jsonify


class MethodsGraph:

    def __init__(self):
        self.method = MethodsCollection()
        self.G = nx.Graph()
        self.indexGraph = 0
        self.title = None
        self.index = 0
        self.recommend_article = None

    def update_graph(self, article):

        count = self.indexGraph

        self.G.add_node(self.indexGraph)
        self.G.nodes[count]['source'] = article["source"]
        self.G.nodes[count]["author"] = article["author"]
        self.G.nodes[count]["title"] = article["title"]
        self.G.nodes[count]["description"] = article["description"]
        self.G.nodes[count]["url"] = article["url"]
        self.G.nodes[count]["urlToImage"] = article["urlToImage"]
        self.G.nodes[count]["publishedAt"] = article["publishedAt"]
        self.G.nodes[count]["content"] = article["content"]

        if self.title == article['title']:
            self.index = count
            print(self.index)

        self.indexGraph += 1

        author = self.G.nodes[count]["author"]
        name = self.G.nodes[count]['source']['name']

        for i in list(self.G.nodes.data()):

            if author == i[1]['author']:
                self.G.add_edge(count, i[0])

            elif name == i[1]['source']['name']:
                self.G.add_edge(count, i[0])

    def find_neighbors(self):

        neighbors = self.G.neighbors(self.index)
        max = 0
        index = 0
        for i in neighbors:
            self.index = i
            node = nx.closeness_centrality(self.G, i)
            if (max < node):
                index = i
                max = node

        return index

    def get_all_collections(self):
        collections = []
        names = ['government', 'health', 'economy', 'environment', 'education', 'business',
                 'sport', 'entertainment']

        for name in names:
            collection = self.method.get_collection(name)
            cursor = collection.find({})
            collections.append(collection)

            for article in cursor:
                self.update_graph(article)

    def plot_graph(self):
        nx.draw(self.G)
        plt.show()

    def getArticle(self):

        index = self.find_neighbors()

        return jsonify(self.G[index])
