from accounts.models import Teacher ,Course
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='instructor.user.username', read_only=True)
    photo_url = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Course
        fields = ['id', 'name', 'photo', 'photo_url', 'instructor', 'num_students', 
                 'price', 'num_hours', 'category', 'rate', 'teacher_name']
        extra_kwargs = {
            'photo': {'required': False, 'write_only': True}  # Make photo optional for updates
        }
    
    def get_photo_url(self, obj):
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        return None

    def update(self, instance, validated_data):
        # If photo isn't provided, keep the existing one
        if 'photo' not in validated_data:
            validated_data['photo'] = instance.photo
        return super().update(instance, validated_data)