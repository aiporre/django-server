from rest_framework import serializers
from .models import Cat, Details



# a Cat is a user that has its details..
class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ('id','cat_name','pub_date')

# a Cat has Details that are editable by the user in MyProfile site.
class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ('id','cat','description','age','likes','picturelink')

# Cat is connected with the datails to have only rest endpoint
class CatDetailsSerializer(serializers.ModelSerializer):
    cat = CatSerializer(read_only=True)
    class Meta:
        model = Details
        fields = ('id','cat','description','age','likes','picturelink')
