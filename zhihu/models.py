from django.db import models
from datetime import timezone
from django.core import serializers
from django.conf import settings
import inspect
import datetime

from django.shortcuts import get_object_or_404


class BaseManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(is_deleted=False, is_active=True)

    def delete(self):
        pass


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(null=True, blank=True)

    objects = BaseManager()
    serializable_fields = ["id", "is_active"]

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        using = kwargs.get('using', settings.DATABASES['default'])
        models.signals.pre_delete.send(sender=self.__class__, instance=self, using=using)
        count = 0
        # self.deleted_at = timezone.now()
        # self.is_deleted = True
        # self.save()
        count = 1
        all_related = [
            f for f in self._meta.get_fields() if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
        ]

        for related in all_related:
            rel = related.get_accessor_name()
            if not hasattr(self, rel):
                return

            related_manager = getattr(self, rel)
            try:
                if related.one_to_one:
                    related_manager.delete()
                else:
                    related_manager.all().delete()
            except Exception as e:
                related_manager.__class__.objects.all().delete()

        models.signals.post_delete.send(sender=self.__class__, instance=self, using=using)
        return count

    def to_dict(self):
        if not hasattr(self, "serializable_fields"):
            return {}
        serializable_fields = getattr(self, "serializable_fields")
        return dict(zip(serializable_fields, [getattr(self, attr) for attr in serializable_fields]))


def base_model_delete(request, model, pk):
    instance = get_object_or_404(model, pk=pk)
    count = instance.delete()
    return {"success": bool(count), "count": count}


def base_model_update(request, model_instance):
    post = request.POST
    posted_keys = post.keys()
    fields = model_instance.serializable_fields
    try:
        for key in set.intersection(posted_keys, fields):
            if hasattr(model_instance, key):
                setattr(model_instance, key, post.get(key))
        model_instance.save()
        return 1
    except:
        return 0


def base_model_create(request, model_cls):
    model = model_cls()
    base_model_update(request, model)


def get_model_list(request, model, page, page_size):
    post = request.POST
    kwargs = {}

    if not hasattr(model, "serializable_fields"):
        return [], 0

    for key in model.serializable_fields:
        if key in post:
            # kwargs[key] = post.get(key)
            field_type = model._meta.get_field(key).get_internal_type()
            if field_type == "CharField":
                kwargs[key + "__icontains"] = "".join(list(post.get(key)))
            elif field_type == "DateTimeField":
                now = datetime.datetime.now()
                delta = datetime.timedelta(days=3)
                kwargs[key + "__gte"] = now - delta
            elif field_type == "BooleanField":
                kwargs[key] = "True"

    page = int(page)
    page_size = int(page_size)
    offset = (page - 1) * page_size

    query_set = model.objects.filter(**kwargs)
    return query_set[offset: offset + page_size], query_set.all().count()
