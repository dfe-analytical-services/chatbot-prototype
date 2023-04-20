import sys
sys.path.append('C:/Users/JSHARRATT/Documents/gpt4-langchain-dfe/backend//django_proj/api')

from django.test import TestCase
from api import makechain
import pinecone
from langchain.vectorstores.pinecone import Pinecone
from unittest.mock import MagicMock, patch
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.embeddings import OpenAIEmbeddings
from api.makechain import make_chain


class MyViewTests(TestCase):
    
    @patch("pinecone.init")
    @patch("builtins.print")
    def test_init_pine_success(self, mock_print, mock_pinecone_init):
        # Configure the mock to not raise any exceptions
        mock_pinecone_init.return_value = None

        makechain.init_pine()

        # Check that pinecone.init was called with the correct arguments
        mock_pinecone_init.assert_called_with(api_key='',
                                              environment="northamerica-northeast1-gcp")

        # Check that 'Pinecone Initilaised successfully' was printed
        mock_print.assert_called_with('Pinecone Initilaised successfully')
        
        
    @patch("pinecone.init")
    @patch("builtins.print")
    def test_init_pine_exception(self, mock_print, mock_pinecone_init):
        # Configure the mock to raise an exception
        sample_error = Exception("Sample error message")
        mock_pinecone_init.side_effect = sample_error

        makechain.init_pine()

        # Check that 'Error' and the error message were printed
        mock_print.assert_called_with('Error', sample_error)
