"""
Repository أساسي عام (Generic Base Repository).
كل Repository خاص بجدول معيّن يرث من هذا الكلاس ويحدّد model الخاص به.
"""
from app.extensions import db


class BaseRepository:
    model = None

    def get_by_id(self, record_id):
        return self.model.query.get(record_id)

    def get_all(self):
        return self.model.query.all()

    def create(self, **kwargs):
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance

    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
