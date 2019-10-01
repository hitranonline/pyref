from django.forms import ModelForm, ValidationError
from .models import Ref

class RefForm(ModelForm):
    class Meta:
        model = Ref
        exclude = ['ris', 'citeproc_json']

    def clean_doi(self):
        doi = self.cleaned_data['doi']
        try:
            ref = Ref.objects.get(doi=doi)
            if ref.pk != self.instance.pk:
                raise ValidationError('A reference with this DOI exists in'
                                            ' the database already')
        except Ref.MultipleObjectsReturned:
            # Hmmm... there are already multiple entries with this DOI in the
            # database. TODO deal with this case
            pass
        except Ref.DoesNotExist:
            # Good: a reference with this DOI is not in the DB already
            pass

        return self.cleaned_data['doi']
