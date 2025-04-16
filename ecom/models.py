from django.db import models
from django.contrib.auth.models import User
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


# class Product(models.Model):
#     name=models.CharField(max_length=100)
#     product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
#     price = models.PositiveIntegerField()
#     description=models.CharField(max_length=500)
#     def __str__(self):
#         return self.name

class Product(models.Model):
    uid = models.CharField(max_length=100, unique=True , blank=True, null=True)
    name = models.CharField(max_length=500 , blank=True, null=True)
    model = models.CharField(max_length=255 , blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255 , blank=True, null=True)
    # SIZE is stored as a comma-separated string
    size = models.CharField(max_length=255, help_text="Comma-separated sizes" , blank=True, null=True)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    

    AGE_GROUP_CHOICES = (
        ('Adult', 'Adult'),
        ('Kid', 'Kid'),
    )
    # age_group = models.CharField(max_length=5, default='Adult', choices=AGE_GROUP_CHOICES)
    age_group = models.CharField(max_length=255, choices=AGE_GROUP_CHOICES, default='Adult')

    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)
    product=models.ForeignKey('Product',on_delete=models.CASCADE,null=True)
    email = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=500,null=True)
    mobile = models.CharField(max_length=20,null=True)
    order_date= models.DateField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

def get_similar_products(current_product, all_products, top_n=5):
    # Build list of all descriptions
    descriptions = [product.name for product in all_products]
    
    # Vectorize descriptions
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(descriptions)

    # Get index of current product
    current_index = list(all_products).index(current_product)

    # Compute cosine similarity
    cosine_similarities = linear_kernel(tfidf_matrix[current_index:current_index+1], tfidf_matrix).flatten()

    # Get indices of top similar products (excluding itself)
    similar_indices = cosine_similarities.argsort()[::-1][1:top_n+1]

    similar_products = [all_products[i] for i in similar_indices]

    return similar_products
