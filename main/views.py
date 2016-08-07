import json

from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateResponseMixin, TemplateView
from registration.forms import RegistrationForm

from .models import Model3D, User


class UserForm(RegistrationForm):
    """
    Override default registration form to handle custom user model
    """
    class Meta:
        model = User
        fields = RegistrationForm.Meta.fields


class UploadForm(ModelForm):
    """
    Form to upload a new model.
    """
    class Meta(object):
        model = Model3D
        fields = ['name', 'data']


class HomePage(View, TemplateResponseMixin):
    """
    Home page list all model with a form to upload a new one
    """
    template_name = "homepage.html"

    def data(self, form=None):
        return {
            'upload_form': form or UploadForm(),
            'models': Model3D.objects.all()
        }

    def get(self, request):
        return self.render_to_response(self.data())

    def post(self, request):
        """
        Handle upload of models
        """
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save(commit=False)
            model.owner = request.user
            model.save()
            return redirect('homepage')
        else:
            return self.render_to_response(self.data(form))


class ModelView(TemplateView):
    """
    Detail page for a model
    """
    template_name = "model.html"

    def get_context_data(self, model_id):
        model = Model3D.objects.get(pk=model_id)
        model.inc_views()

        return {
            'model': model
        }


def badge_list(request):
    """
    Return user's badges in JSON
    """
    result = [badge.name for badge in request.user.badge_set.all()]
    return HttpResponse(json.dumps(result), content_type='application/json')
