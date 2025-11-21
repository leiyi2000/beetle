from tortoise import Model, fields


class Task(Model):
    id = fields.IntField(primary_key=True)
    src = fields.CharField(max_length=512)
    dst = fields.CharField(max_length=512)
    interval = fields.IntField()
    cleanup = fields.BooleanField()
    status = fields.CharField(max_length=64)
    parallel_max = fields.IntField(default=5)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = (("src", "dst"),)
