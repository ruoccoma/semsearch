# Massimiliano Ruocco (ruocco@idi.ntnu.no)
#
# Class providing functionality for indexing/searching dense representation of text (high dimensional features). 
# Core functionality are based on the annoy ANN search developed here https://github.com/spotify/annoy

from pandas import HDFStore,DataFrame
from annoy import AnnoyIndex
import pickle
import doc2vec
import os
import time

class Search(object):
	# Attributes
	DATA_NAME_H5 = 'data'
	COLUMN_NAME_H5 = 'state'
	FEAT_DIM = 2048
	N_TREES = 10
	DICT_INT2STR = "./models/dict.pickle"
	DICT_STR2INT = "./models/dict_inv.pickle"
	INDEX_FILE = './models/index.ann'

	index_dict_int2str = dict()
	index_dict_str2int = dict()
	index = AnnoyIndex(FEAT_DIM)
	#inputfile_h5 = './data/titles_d2v_300.h5'

	def __init__(self,inputfolder_h5 = None):
		if inputfolder_h5 == None:
			self.index_dict_int2str = pickle.load(open(self.DICT_INT2STR, "rb"))
			self.index_dict_str2int = pickle.load(open(self.DICT_STR2INT, "rb"))
			self.index.load(self.INDEX_FILE)
		else:
			count = 0
			start = time.clock()
			input_files = os.listdir(inputfolder_h5)
			for file in input_files:
				if(file.endswith(".h5")):
					hdf = HDFStore(inputfolder_h5 + os.sep + file)
					if(len(hdf.keys()) >0 ):
						#print(file)
						l = len(hdf[self.DATA_NAME_H5])
						val_list = hdf[self.DATA_NAME_H5][self.COLUMN_NAME_H5]
						ind_list = hdf[self.DATA_NAME_H5].index
						for i in range(0,l):
							val = val_list[i].tolist()
							ind = ind_list[i]
							count = count + 1
							self.index.add_item(i, val)
							#print(i)
							self.index_dict_int2str[i] = ind
							self.index_dict_str2int[ind] = i
						hdf.close()
			end = time.clock()
			print(str(count))
			print("Indexing time: " + str(end-start))
			start = time.clock()
			self.index.build(self.N_TREES)
			self.index.save(self.INDEX_FILE)
			pickle.dump(self.index_dict_int2str, open( self.DICT_INT2STR, "wb" ))
			pickle.dump(self.index_dict_str2int, open( self.DICT_STR2INT, "wb" ))
			end = time.clock()
			print("Index storing time: " + str(end-start))

	def get_nns_by_query(self, query, topk):
		vec = doc2vec.map(query)
		return self.get_nns_by_vec(vec, topk)

	def get_nns_by_id(self, id, topk):
		id_item = self.index_dict_str2int.get(id)
		res = self.index.get_nns_by_item(id_item, topk, include_distances=True)
		l = len(res[0])
		for i in range(0,l):
			res[0][i] = self.index_dict_int2str.get(res[0][i])
		return res

	def get_nns_by_vec(self, v, topk):
		res = self.index.get_nns_by_vector(v, topk, include_distances=True)
		l = len(res[0])
		for i in range(0,l):
			res[0][i] = self.index_dict_int2str.get(res[0][i])
		return res

		
