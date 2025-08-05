from rest_framework import serializers
from .models import User, Student, Teacher, Parent
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)
    biography = serializers.CharField(required=False, allow_blank=True)

    # Optional fields
    national_id = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)
    date_of_birth = serializers.DateField(required=False)
    rate = serializers.FloatField(required=False, read_only=True)
    grade = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'user_type',
            'biography', 'national_id', 'photo', 'date_of_birth',
            'rate', 'grade'
        ]

    def validate(self, data):
        user_type = data.get('user_type')

        if user_type == 'student':
            if 'grade' not in data:
                raise serializers.ValidationError({"grade": "Grade is required for students."})
        elif user_type == 'teacher':
            if 'rate' not in data:
                data['rate'] = 0  # Default rate
        elif user_type == 'parent':
            if 'national_id' not in data:
                raise serializers.ValidationError({"national_id": "You must provide your child's national ID."})

        return data

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')
        national_id = validated_data.pop('national_id', None)
        photo = validated_data.pop('photo', None)
        date_of_birth = validated_data.pop('date_of_birth', None)
        biography = validated_data.pop('biography', '')
        rate = validated_data.pop('rate', 0)
        grade = validated_data.pop('grade', None)

        # Create base User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            user_type=user_type,
            biography=biography
        )
        user.set_password(password)
        user.save()

        # Create related profile
        if user_type == 'student':
            Student.objects.create(
                user=user,
                national_id=national_id,
                photo=photo,
                date_of_birth=date_of_birth,
                grade=grade
            )
        elif user_type == 'teacher':
            Teacher.objects.create(
                user=user,
                national_id=national_id,
                photo=photo,
                date_of_birth=date_of_birth,
                rate=rate,
                biography=biography
            )
        elif user_type == 'parent':
            try:
                student = Student.objects.get(national_id=national_id)
            except Student.DoesNotExist:
                raise serializers.ValidationError({"student": "No student found with this national ID."})
            Parent.objects.create(
                user=user,
                student=student
            )

        return user



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "user_type": user.user_type,
            "user": user
        }

class LoginResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    user_type = serializers.CharField()
    tokens = serializers.DictField()
