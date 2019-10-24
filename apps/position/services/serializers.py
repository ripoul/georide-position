from rest_framework import serializers


__all__ = ['PositionSerializer', 'TokenSerializer']

class PositionSerializer(serializers.Serializer):
    trackerId = serializers.IntegerField()
    from_ = serializers.DateTimeField()
    to = serializers.DateTimeField()

    def to_representation(self, instance):
        data = super(PositionSerializer, self).to_representation(instance)
        from_ = data.pop('from_')
        data['from'] = from_
        return data


class TokenSerializer(serializers.Serializer):
    authToken = serializers.CharField()


class TrackSerializer(serializers.Serializer):
    tracker_id = serializers.IntegerField(source='trackerId')
    tracker_name = serializers.CharField(source='trackerName')

