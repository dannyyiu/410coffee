from django.db import models


class TestAPI(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()

    #permission fields
    owner = models.ForeignKey('auth.User', related_name='testapi')
    highlighted = models.TextField()

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        "Add values to highlighted"
        self.highlighted = "----"+self.code+"----"
        super(TestAPI, self).save(*args, **kwargs)