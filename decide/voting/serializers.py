from rest_framework import serializers

from .models import Question, QuestionOption, Voting, ScoreQuestion, ScoreQuestionOption, ScoreVoting
from base.serializers import KeySerializer, AuthSerializer


class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')

class ScoreQuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScoreQuestionOption
        fields = ('number', 'option')

class ScoreQuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = ScoreQuestionOptionSerializer(many=True)
    class Meta:
        model = ScoreQuestion
        fields = ('desc', 'options')


class ScoreVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = ScoreQuestionSerializer(many=False)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = ScoreVoting
        fields = ('id', 'name', 'desc', 'question', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class ScoreSimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    question = ScoreQuestionSerializer(many=False)

    class Meta:
        model = ScoreVoting
        fields = ('name', 'desc', 'question', 'start_date', 'end_date')

