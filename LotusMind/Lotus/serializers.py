from rest_framework import serializers
from django.contrib.auth.models import User


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    id_usuario = serializers.ReadOnlyField()
    nombre_usuario = serializers.CharField(max_length=100)
    correo_usuario = serializers.CharField()
    tipo_usuario = serializers.CharField()
    contraseña_usuario = serializers.CharField()

    def create(self, validate_data):
        instance = User()
        instance.nombre_usuario = validate_data.get('nombre_usuario')
        instance.correo_usuario = validate_data.get('correo_usuario')
        instance.tipo_usuario = validate_data.get('tipo_usuario')
        instance.set_password(validate_data.get('password'))
        instance.save()
        return instance

    def validate_usuario(self, data):
        usuarios = User.objects.filter(correo_usuario=data)
        if len(usuarios) != 0:
            raise serializers.ValidationError("Este correo ya esta usado")
        else:
            return data
