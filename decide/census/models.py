from django.db import models


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    votingTypes = (('V', 'Voting'), ('BV', 'BinaryVoting'))
    type = models.CharField(max_length=2, choices=votingTypes, default='V')

    class Meta:
        unique_together = (('voting_id', 'voter_id','type'),)
