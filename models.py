from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Chat(Model):
    id = fields.BigIntField(pk=True)
    title = fields.TextField(null=True)
    invite_link = fields.CharField(max_length=100)
    type = fields.CharField(max_length=100)

    class Meta:
        table = "chat"

    def __str__(self):
        return self.name


class MessageQueue(Model):
    id = fields.IntField(pk=True)
    chat = fields.ForeignKeyField('models.Chat', related_name='messages')
    text = fields.TextField()
