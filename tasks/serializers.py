from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # returns the username instead of the id
    # owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Task
        fields = ['id', 'owner', 'title', 'description',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def validate_title(self, v):
        v = v.strip()
        if len(v) < 3:
            raise serializers.ValidationError(
                "Ensure this field has at least 3 characters.")
        return v

    # This does not work because the field's choices are validated before this method is called,
    # so this function will never be executed.
    def validate_status(self, value):
        valid_choices = [choice[0] for choice in Task.Status.choices]
        if value not in valid_choices:
            raise serializers.ValidationError(
                f"{value} is not a valid choice. Allowed values: {valid_choices}"
            )
        return value
