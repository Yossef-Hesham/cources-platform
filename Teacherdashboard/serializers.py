from accounts.models import Teacher ,Course
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()  # More flexible than CharField
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'photo', 'photo_url', 'instructor', 
                'num_students', 'price', 'num_hours', 'category', 
                'rate', 'teacher_name']
        extra_kwargs = {
            'photo': {'required': False, 'write_only': True},
            'instructor': {'read_only': True}  # Prevent accidental assignment
        }

    def get_teacher_name(self, obj):
        # Safe access to nested relation
        return getattr(getattr(obj.instructor, 'user', None), 'username', None)

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo and request:
            return request.build_absolute_uri(obj.photo.url)
        return None

    def update(self, instance, validated_data):
        if 'photo' not in validated_data:
            validated_data['photo'] = instance.photo
        return super().update(instance, validated_data)