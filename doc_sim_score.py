import sys, re, argparse
from collections import Counter


def parse_args():
	parser = argparse.ArgumentParser(description='Parse arguments for document similarity program.')
	parser.add_argument('first_document')
	parser.add_argument('second_document')
	parser.add_argument('-e', '--embedding_type', type=str, choices={'counts', 'context-counts'}, default='counts',
			help='Word Embedding Type:\n\t \
				1)\'counts\': use raw counts of each word as to encode document embedding \
				2)\'context-counts\': use counts of context words to encode a word embedding for each given word, for a given window size around that word.')
	parser.add_argument('-w', '--window_size', type=int, choices=range(1, 11), default=2,
			help='Window Size: size of context window before and after each word, used if --embedding_type is \'context-counts\' ')
	args = parser.parse_args()
	return args

def read_doc(document):
	with open(document, "r") as df:
		docstr = df.read()

	return docstr


def _magnitude(a):
	'''
		Get magnitude of vector in Counter form
	'''
	return ((sum(x ** 2 for x in a.values())) ** 0.5)

def _dot_product(a, b):
	'''
		Get dot product of vector in Counter form
	'''
	mutual_words = a.keys() & b.keys()
	return sum(a[word] * b[word] for word in mutual_words)

def _cosine_sim(a, b):
	return (_dot_product(a, b) / (_magnitude(a) * _magnitude(b)))

def doc_sim(a, b, word_embedding_type='counts'):
	'''
		Get similarity between 2 documents
		If word embedding type is counts, simply treat each document as a bag of words
		If word embedding type is context-counts, take an average over the similarity
			between each word embedding defined by the words seen in its context
	'''
	if word_embedding_type == 'counts':
		return _cosine_sim(a, b)

	if word_embedding_type == 'context-counts':
		# Average over cos-sim of each word embedding
		mutual_words = a.keys() & b.keys()
		summed_cos_sim = sum(_cosine_sim(a[word], b[word]) for word in mutual_words)
		return 0 if len(mutual_words) == 0 else summed_cos_sim / len(mutual_words)

	raise ValueError('Invalid word embedding type.')

def _get_count_word_embeddings_from_doc(doc_tokens):
	'''
		Get document embedding as a Counter of words
		NOTE: Will not encode word order
	'''
	wordEmbeddings = Counter()

	# Count each token
	for token in doc_tokens:
		wordEmbeddings[token] += 1

	return wordEmbeddings

def _get_context_word_embeddings_from_doc(doc_tokens, window):
	'''
		Get document embedding as nested Counters
		Each word stores the counts of context words found surrounding it
	'''
	num_tokens = len(doc_tokens)

	# Initialize word embeddings
	wordEmbeddings = dict()
	for word in doc_tokens:
		wordEmbeddings[word] = Counter()

	# Iterate over words
	for i in range(num_tokens):
		curr_word = doc_tokens[i]

		# Slide a context window over each word
		for j in range(max(i-window, 0), min(i+window+1, num_tokens) ):
			# Don't count same word
			if j == i: continue

			near_word = doc_tokens[j]
			wordEmbeddings[curr_word][near_word] += 1

	return wordEmbeddings

def get_word_embeddings_from_doc(docstr, word_embedding_type='counts', window=2):
	# Pad punctuation with whitespace
	docstr = re.sub('([.,!?()])', r' \1 ', docstr)
	docstr = re.sub('\n', r'', docstr)
	tokens = docstr.split()

	if word_embedding_type == 'counts':
		return _get_count_word_embeddings_from_doc(tokens)
	elif word_embedding_type == 'context-counts':
		return _get_context_word_embeddings_from_doc(tokens, window)

	raise ValueError('Invalid word embedding type.')

def calculate_similarity(docstr_A, docstr_B, word_embedding_type='counts', window=2):
	################ Get embeddings for each document #################
	embedding_A = get_word_embeddings_from_doc(docstr_A, word_embedding_type=word_embedding_type, window=window)
	embedding_B = get_word_embeddings_from_doc(docstr_B, word_embedding_type=word_embedding_type, window=window)

	################# Compute similarity score between documents #################
	similarity = doc_sim(embedding_A, embedding_B, word_embedding_type=word_embedding_type)
	return similarity

def main():
	################ Parse Arguments #################
	args = parse_args()
	doc_A = args.first_document
	doc_B = args.second_document
	word_embedding_type = args.embedding_type
	window = args.window_size
	docstr_A = read_doc(doc_A)
	docstr_B = read_doc(doc_B)

	################ Calculate Document Similarity #################
	similarity = calculate_similarity(docstr_A, docstr_B, word_embedding_type=word_embedding_type, window=window)
	print("Document similarity: {:.6f}".format(similarity))

if __name__ == '__main__':
	main()