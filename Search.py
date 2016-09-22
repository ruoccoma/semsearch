# Massimiliano Ruocco (ruocco@idi.ntnu.no)
#
# Class providing functionality for indexing/searching dense representation of text (high dimensional features). 
# Core functionality are based on the annoy ANN search developed here https://github.com/spotify/annoy

from pandas import HDFStore,DataFrame
from annoy import AnnoyIndex
import pickle

class Search(object):
	# Attributes
	DATA_NAME_H5 = 'data'
	COLUMN_NAME_H5 = 'feats'
	FEAT_DIM = 2048
	N_TREES = 10
	DICT_INT2STR = "dict.pickle"
	DICT_STR2INT = "dict_inv.pickle"
	INDEX_FILE = 'index.ann'

	index_dict_int2str = dict()
	index_dict_str2int = dict()
	index = AnnoyIndex(FEAT_DIM)
	#inputfile_h5 = './data/titles_d2v_300.h5'

	def __init__(self,inputfile_h5 = None):
		if inputfile_h5 == None:
			self.index_dict_int2str = pickle.load(open(self.DICT_INT2STR, "rb"))
			self.index_dict_str2int = pickle.load(open(self.DICT_STR2INT, "rb"))
			self.index.load(self.INDEX_FILE)
		else:
			hdf = HDFStore(inputfile_h5)
			l = len(hdf[self.DATA_NAME_H5])
			count = 0
			val_list = hdf[self.DATA_NAME_H5][self.COLUMN_NAME_H5]
			ind_list = hdf[self.DATA_NAME_H5].index
			for i in range(0,l):
				val = val_list[i].tolist()
				ind = ind_list[i]
				self.index.add_item(i, val)
				print(i)
				self.index_dict_int2str[i] = ind
				self.index_dict_str2int[ind] = i
			self.index.build(self.N_TREES)
			self.index.save(self.INDEX_FILE)
			pickle.dump(self.index_dict_int2str, open( self.DICT_INT2STR, "wb" ))
			pickle.dump(self.index_dict_str2int, open( self.DICT_STR2INT, "wb" ))
			hdf.close()

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

		
