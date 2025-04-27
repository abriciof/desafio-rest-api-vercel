from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_validation.validate_password],
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "username",      # agora obrigatório
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "profile_image": {"required": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("password_confirm"):
            raise serializers.ValidationError({"password_confirm": _("As senhas não conferem.")})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            password=validated_data["password"],
            profile_image=validated_data.get("profile_image"),
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[password_validation.validate_password],
        style={"input_type": "password"},
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Senha atual incorreta."))
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile_image", "email_confirmed"]
        read_only_fields = ["id", "email_confirmed"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True,
        style={"input_type": "password"}
    )


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class EmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(_("Usuário com esse e-mail não existe."))
        return value


class VerifyEmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email__iexact=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": _("E-mail não cadastrado.")})
        attrs["user"] = user
        return attrs
    
    
class GoogleAuthSerializer(serializers.Serializer):
    """
    Recebe o ID-token JWT do Google.
    """
    id_token = serializers.CharField(write_only=True, required=True)