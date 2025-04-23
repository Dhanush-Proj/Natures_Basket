from django import forms
from .models import Product, Image, Variant, Stock, Category, Subcategory

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_image']
    def clean(self):
            cleaned_data = super().clean()
            if 'category_image' in cleaned_data:
                del cleaned_data['category_image'] #remove image from validation
            return cleaned_data

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category', 'name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'subcategory',
            'name',
            'description',
            'price',
            'is_active',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    variants = forms.CharField(widget=forms.Textarea, required=False, label="Variants (e.g., Size:S,M,L; Color:Red,Green,Blue)")

    def clean_variants(self):
        variants_text = self.cleaned_data.get('variants', '')
        if variants_text:
            variant_sets = variants_text.strip().split(';')
            for variant_set in variant_sets:
                if variant_set.strip():
                    try:
                        name, values = variant_set.split(':', 1)
                        values = values.strip().split(',')
                        if not name or not values:
                            raise forms.ValidationError("Variants must include both a name and values.")
                    except ValueError:
                        raise forms.ValidationError("Invalid variant format. Use 'Name:Value1,Value2;Name2:Value1' format.")
        return variants_text

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()

        variants_text = self.cleaned_data.get('variants', '')
        if variants_text:
            variant_sets = variants_text.strip().split(';')
            for variant_set in variant_sets:
                if variant_set.strip():
                    name, values = variant_set.split(':', 1)
                    values = values.strip().split(',')
                    for value in values:
                        variant = Variant.objects.create(product=product, name=name.strip(), value=value.strip())
                        Stock.objects.create(product=product, variant=variant, quantity=0)

        return product

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

ImageFormSet = forms.modelformset_factory(Image, form=ImageForm, extra=0, can_delete=True)  # Start with no extra forms
