

from core import db
from core.models import required_columns

class Mandlebrot(db.Model):

    # Should zoom be included? Where is iterations
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zoom = db.Column(db.Float, nullable=False)
    focusx = db.Column(db.Float(24), nullable=False)
    focusy = db.Column(db.Float(24), nullable=False)
    iterations = db.Column(db.Float, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    # mandlebrot_frame = db.relationship('MandlebrotFrame', backref='frames', lazy=True, cascade='all, delete-orphan')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'zoom': self.zoom,
            'focusx': self.focusx,
            'focusy': self.focusy,
            'iterations': self.iterations,
            'width': self.width,
            'height': self.height,
        }



    def generate(self):
        ''' Return a complete dataset. '''
        real = []
        imaginary = []

        return [real, imaginary]

    # Only save the settings that Start and stop a users saved fractal. Only two save points can be made that links to fractals.
    # This should be implemented on the client side

    @staticmethod
    def create(settings):
        # Define settings as columns to save user generation settings
        required = required_columns(Mandlebrot)
        if (required != list(settings.keys())): return None
        # validate the data types of the fields provided in settings as well (new feature)
        return Mandlebrot(**settings)



# class MandlebrotFrame(db.Model):

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     start = db.Column(db.Integer, db.ForeignKey('mandlebrot.id'), nullable=False)
#     end = db.Column(db.Integer, db.ForeignKey('mandlebrot.id'), nullable=False)
#     speed = db.Column(db.Float(), nullable=False)




# # UserMixin (learn how to automatically add this model as a reference in the User model)
# class UserMandlebrotEntry(db.Model):

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))
#     mandlebrot_id = db.Column(db.Integer, db.ForeignKey('mandlebrot.id'), nullable=False)





# class UserMandlebrotFrame(db.Model):

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id', nullable=False))
#     frame_id = db.Column(db.Integer, db.ForeignKey('mandlebrot_frame.id'), nullable=False)




