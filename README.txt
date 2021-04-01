--- Document Similarity Comparison Tool ---

Usage:
	Local - python doc_sim_score.py first_document second_document [-e {counts,context-counts}] [-w {1,2,3,4,5,6,7,8,9,10}]

		Examples:
			python doc_sim_score.py data_samples/sample_1.txt data_samples/sample_2.txt -e counts
			python doc_sim_score.py data_samples/sample_1.txt data_samples/sample_2.txt -e context-counts -w 4

		Positional Args:
			frist_document: Text for first document to be compared (on a single line)
			second_document: Text for second document to be compared (on a single line)

		Optional Args:
			-e: Embedding type; either 'counts' or 'context-counts', default is 'counts'
				'counts' treats each document as a bag of words [ignoring word ordering/context]
				'context-counts' treats each word in a document as a collection of its surrounding words for a given window size. Document is a collection of such word 'vectors'

			-w: Window size; defines context window if embedding type is 'context-counts', default is 2

	HTTP Service - python server.py (runs http server listening for requests)

		Once server is running, can send a post request with (newline separated) documents in the text body.  (Similarity is hard coded for embedding_type=context-counts, window_size=2)

		Examples, using curl, from bash:

			EXAMPLE1=$(cat data_samples/example_1.txt)
			curl -X POST -d "$EXAMPLE1" http://localhost:8008

			EXAMPLE2=$(cat data_samples/example_2.txt)
			curl -X POST -d "$EXAMPLE2" http://localhost:8008


--- Requirements ---

python version: python3.x