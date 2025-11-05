"""
Unit tests for password generation logic
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import generate_password


class TestPasswordGeneration:
    """Test password generation function"""
    
    def test_default_password_length(self):
        """Test default password length is 12"""
        password = generate_password()
        assert len(password) == 12
    
    def test_custom_length(self):
        """Test custom password lengths"""
        for length in [4, 8, 16, 32, 64, 128]:
            password = generate_password(length=length)
            assert len(password) == length
    
    def test_minimum_length(self):
        """Test minimum length constraint"""
        password = generate_password(length=4)
        assert len(password) == 4
    
    def test_maximum_length(self):
        """Test maximum length constraint"""
        password = generate_password(length=128)
        assert len(password) == 128
    
    def test_only_lowercase(self):
        """Test password with only lowercase letters"""
        password = generate_password(
            length=20,
            use_uppercase=False,
            use_lowercase=True,
            use_digits=False,
            use_symbols=False
        )
        assert len(password) == 20
        assert password.islower()
        assert password.isalpha()
    
    def test_only_uppercase(self):
        """Test password with only uppercase letters"""
        password = generate_password(
            length=20,
            use_uppercase=True,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False
        )
        assert len(password) == 20
        assert password.isupper()
        assert password.isalpha()
    
    def test_only_digits(self):
        """Test password with only digits"""
        password = generate_password(
            length=20,
            use_uppercase=False,
            use_lowercase=False,
            use_digits=True,
            use_symbols=False
        )
        assert len(password) == 20
        assert password.isdigit()
    
    def test_mixed_characters(self):
        """Test password with mixed character types"""
        password = generate_password(
            length=50,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=True
        )
        assert len(password) == 50
        # At least check it's not all the same type
        assert not password.isalpha()
        assert not password.isdigit()
    
    def test_no_options_selected(self):
        """Test fallback when no character types selected"""
        password = generate_password(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False
        )
        # Should still generate a password (fallback to all types)
        assert len(password) == 12
        assert len(password) > 0
    
    def test_randomness(self):
        """Test that generated passwords are different (randomness)"""
        passwords = [generate_password(length=16) for _ in range(10)]
        # All passwords should be unique
        assert len(set(passwords)) == 10
    
    def test_contains_uppercase(self):
        """Test that password contains uppercase when requested"""
        # Generate multiple to ensure at least one has uppercase
        passwords = [generate_password(length=20, use_uppercase=True, 
                                       use_lowercase=False, use_digits=False, 
                                       use_symbols=False) for _ in range(5)]
        assert all(pwd.isupper() for pwd in passwords)
    
    def test_contains_lowercase(self):
        """Test that password contains lowercase when requested"""
        passwords = [generate_password(length=20, use_uppercase=False, 
                                       use_lowercase=True, use_digits=False, 
                                       use_symbols=False) for _ in range(5)]
        assert all(pwd.islower() for pwd in passwords)
    
    def test_contains_digits(self):
        """Test that password contains digits when requested"""
        passwords = [generate_password(length=20, use_uppercase=False, 
                                       use_lowercase=False, use_digits=True, 
                                       use_symbols=False) for _ in range(5)]
        assert all(pwd.isdigit() for pwd in passwords)
    
    def test_password_strength_variety(self):
        """Test different password configurations"""
        configs = [
            {'length': 8, 'use_uppercase': True, 'use_lowercase': True, 
             'use_digits': False, 'use_symbols': False},
            {'length': 12, 'use_uppercase': True, 'use_lowercase': True, 
             'use_digits': True, 'use_symbols': False},
            {'length': 16, 'use_uppercase': True, 'use_lowercase': True, 
             'use_digits': True, 'use_symbols': True},
        ]
        
        for config in configs:
            password = generate_password(**config)
            assert len(password) == config['length']


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_short_password(self):
        """Test very short password (minimum)"""
        password = generate_password(length=4)
        assert len(password) == 4
    
    def test_very_long_password(self):
        """Test very long password (maximum)"""
        password = generate_password(length=128)
        assert len(password) == 128
    
    def test_single_character_type(self):
        """Test with only one character type enabled"""
        password = generate_password(
            length=10,
            use_uppercase=False,
            use_lowercase=True,
            use_digits=False,
            use_symbols=False
        )
        assert len(password) == 10
        assert all(c.islower() for c in password)
    
    def test_all_character_types(self):
        """Test with all character types enabled"""
        password = generate_password(
            length=50,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_symbols=True
        )
        assert len(password) == 50
