from django import forms
from .models import Image
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests

class ImageCreateForm(forms.ModelForm):
    class Meta:
        #forms based on the Image model with the included fields
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    #validating the extension
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower() #extension is valid?
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
    
    #overriding save() 
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False) #returns instance of image but doesnt saves it
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        #download image from the give URL
        response = requests.get(image_url)
        
        #the file is saved to the media directory but not yet saved to the databased
        image.image.save(image_name, ContentFile(response.content), save=False)

        #saved into the database if commit==True
        if commit:
            image.save()
        #else it saves to the media directory and not the database and returns the image
        return image