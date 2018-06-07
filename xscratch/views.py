'''
xScratch App views
'''
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from xscratch import forms
from xscratch.interpreter.analyser import XSInterpreter
from xscratch.exceptions import XSSyntaxError, XSArduinoError


class IndexView(TemplateView):
    '''
    The starting point for the xScratch

    Redirects to the Homepage
    '''

    def dispatch(self, request, *args, **kwargs):
        '''
        Every request for the IndexView is processed here

        @return: redirect to the HomePage
        '''
        return redirect('xs:home')


class SignUpView(TemplateView):
    '''
    View responsible for the Sign Up feature

    @atrrib: SignUpForm form_class: The sign up form
    @attrib: str template_name: The html template for the view
    '''
    form_class = forms.SignUpForm
    template_name = 'xscratch/sign_up.html'

    def get(self, request, *args, **kwargs):
        '''
        Handles a get request
        Renders the sign up template if there is no user logged in

        @return: redirect to home if there is a user logged in
        @return: renders sign up view is not a user logged in
        '''
        if request.user.is_authenticated:
            return redirect('xs:home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        '''
        Handles a post request
        Add the new user into the system if the user data is valid

        @return: redirect to sign in view
        @raises: ValidationError if user data is invalid
        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
        # TODO: handle invalid form data
        return redirect('xs:sign_in')


class SignInView(TemplateView):
    '''
    View responsible for the Sign In feature

    @atrrib: SignInForm form_class: The sign in form
    @attrib: str template_name: The html template for the view
    '''
    form_class = forms.SignInForm
    template_name = 'xscratch/sign_in.html'

    def get(self, request, *args, **kwargs):
        '''
        Handles a get request
        Renders the sign in template if there is no user logged in

        @return: redirect to home if there is a user logged in
        @return: renders sign in view is not a user logged in
        '''
        if request.user.is_authenticated:
            return redirect('xs:home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        '''
        Handles a post request
        Add the new user into the system if the user data is valid

        @return: redirect to HomePage
        @raises: ValidationError if login data is invalid
        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print("User {} logged".format(user))
        # TODO: handle invalid form data
        return redirect('xs:home')


class SignOutView(LoginRequiredMixin, TemplateView):
    '''
    View responsible for the Sign Out feature
    '''

    def get(self, request, *args, **kwargs):
        '''
        Handles a get request
        Logout the user and redirect to the sign_in view

        @return: redirect to the sign in view
        '''
        logout(request)
        return redirect('xs:sign_in')


class HomeView(LoginRequiredMixin, TemplateView):
    '''
    xScratch app homepage

    @attrib: str template_name: homepage's html template path
    '''
    template_name = 'xscratch/home.html'


class ScriptView(LoginRequiredMixin, TemplateView):
    '''
    xScratch app script view

    @attrib: str template_name: script's html template path
    '''
    form_class = forms.ScriptForm
    template_name = 'xscratch/script.html'

    def get(self, request, *args, **kwargs):
        '''
        Handles a get request
        Renders the script template

        @return: renders scripting view
        '''
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        '''
        Handles a post request
        Compiles the script and return the output to the view

        @return: renders the script page with the output on the context
        @raises: ValidationError if script data is invalid
        '''
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            script = form.cleaned_data['script_str']
            interpreter = XSInterpreter(script)
            output = 'fail'
            try:
                interpreter.read()
                output = script.splitlines()
                print(output)
            except XSSyntaxError:
                pass
            except XSArduinoError:
                pass
        return render(request, self.template_name, {'script_output': output, 'form': form})


class LearnView(LoginRequiredMixin, TemplateView):
    '''
    xScratch app learn view

    @attrib: str template_name: learn's html template path
    '''
    template_name = 'xscratch/learn.html'
