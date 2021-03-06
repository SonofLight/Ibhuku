#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import pytest
import factory
import factory.django

from users.tests.factories import UserFactory
from users.models import User
from users.forms import UserRegistrationForm


@pytest.mark.django_db
class TestUserRegisrationForm:
    """
    Test of User Registration Form.
    """

    def setup(self):
        """
        Sets up test fixtures using Factory Boy instances. See factories.py module
        for more information.
        """
        self.form = UserRegistrationForm()
        self.user = UserFactory()
        self.data = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'password': self.user.password,
            'confirm_password': self.user.password,
            'acct_type': 'IND',
            'toc': True,
        }

    def test_user_registration_form_is_not_bound(self):
        """
        Test if form is bound by passed data.
        """
        assert self.form.is_bound == False, 'Returns False if form is not bound by data.(no values passed)'

    def test_user_registration_form_is_bound(self):
        """
        Test if form is bound by passed data.
        """
        self.form = UserRegistrationForm(data={})

        # As per Django documentation, the data={} will return True even if no
        # kwargs passed.
        assert self.form.is_bound == True, 'Returns True if form is bound by data.'

    def test_user_registration_form_is_valid(self):
        """
        Test .is_valid() of form.
        """
        # Test will fail without hard coded kwargs
        form = UserRegistrationForm(data={
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'McTesty@testing.com',
            'password': 'testpassword1234',
            'confirm_password': 'testpassword1234',
            'acct_type': 'IND',
            'toc': True,
        })
        assert form.is_valid() == True, 'Returns True if form is valid.'

    def test_user_registration_form_errors(self, client):
        """
        Test form errors.
        """
        self.form = UserRegistrationForm(data={})

        assert 'This field is required.' in self.form[
            'first_name'].errors, 'Reports error on form field.'
        assert 'This field is required.' in self.form[
            'email'].errors, 'Reports error on form field.'

    def test_user_registration_form_clean_methods(self):
        """
        Test form clean methods.
        """
        form = UserRegistrationForm(data=self.data)

        # instantiate form.is_valid() in order to run clean methods.
        form.is_valid()

        assert 'testpassword0004' in form.clean_password(), 'Returns password.'
        assert 'testpassword0004' in form.cleaned_data.get(
            'password'), 'Returns password if found in cleaned_data'

    def test_user_registration_password_field_validation_error(self):
        """
        Test form password length validation.
        """
        form = UserRegistrationForm(data={
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'McTesty@testing.com',
            'password': 'tests',
            'confirm_password': 'testpassword1234',
            'acct_type': 'IND',
            'toc': True,
        })
        assert form.has_error(
            'password', code='password_short') == True, 'Returns True if length validation error.'

    def test_user_registration_password_field_match_validation(self):
        form = UserRegistrationForm(data={
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': 'McTesty@testing.com',
            'password': 'testpassword0004',
            'confirm_password': 'testpassword1234',
            'acct_type': 'IND',
            'toc': True,
        })
        assert form.non_field_errors() == [
            "Passwords don't match. Please check and try again."], 'Returns validation error for matching pass/cofirm_pass'
