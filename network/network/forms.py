from django import forms
from django.forms import ModelForm
from network.models import Post






class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'body'
        ]

        labels = {'body': "What's on your mind?"}

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control body', 'rows': '3', 'columns': '15'})
        }


# class AuctionListingForm(ModelForm):
#     class Meta:
#         model = AuctionListing
#         fields = [
#             'item_name',
#             'item_description',
#             'category',
#             'starting_bid',
#             'item_pic',
#             'poster'
#         ]

#         widgets = {
#             'item_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'item_description': forms.Textarea(attrs={'class': 'form-control'}),
#             'category': forms.Select(attrs={'class': 'form-control'}),
#             'starting_bid': forms.NumberInput(attrs={'class': 'form-control'}),
#             # 'item_pic': forms.ClearableFileInput(), 
#             'poster': forms.HiddenInput()
#         }
