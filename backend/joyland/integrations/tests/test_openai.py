"""Tests for OpenAI integration."""

from django.test import TestCase, override_settings
from unittest.mock import patch, MagicMock
from joyland.integrations.openai import OpenAIClient, get_default_model


class OpenAISettingsTests(TestCase):
    """Test OpenAI settings and model selection."""
    
    def test_default_model_without_gpt5(self):
        """Test default model selection with GPT-5 disabled."""
        with override_settings(ENABLE_GPT5_MINI=False):
            self.assertEqual(get_default_model(), 'gpt-4')
    
    def test_default_model_with_gpt5(self):
        """Test default model selection with GPT-5 enabled."""
        with override_settings(ENABLE_GPT5_MINI=True):
            self.assertEqual(get_default_model(), 'gpt-5-mini')
    
    def test_model_override(self):
        """Test client respects model override."""
        client = OpenAIClient(model='custom-model')
        self.assertEqual(client.model, 'custom-model')


class OpenAIClientTests(TestCase):
    """Test OpenAI client methods."""
    
    def setUp(self):
        self.client = OpenAIClient()
    
    @patch('openai.Completion.create')
    def test_completion(self, mock_complete):
        """Test completion generation."""
        mock_response = {
            'choices': [{'text': 'Test response'}],
            'usage': {'total_tokens': 10}
        }
        mock_complete.return_value = mock_response
        
        response = self.client.complete('Test prompt')
        
        mock_complete.assert_called_once()
        self.assertEqual(response, mock_response)
    
    @patch('openai.Embedding.create')
    def test_embedding(self, mock_embed):
        """Test embedding generation."""
        mock_response = {
            'data': [{'embedding': [0.1, 0.2, 0.3]}]
        }
        mock_embed.return_value = mock_response
        
        response = self.client.embed('Test text')
        
        mock_embed.assert_called_once()
        self.assertEqual(response, mock_response)
    
    @patch('openai.Completion.create')
    def test_completion_error_handling(self, mock_complete):
        """Test error handling in completion."""
        mock_complete.side_effect = Exception('API error')
        
        with self.assertRaises(Exception):
            self.client.complete('Test prompt')