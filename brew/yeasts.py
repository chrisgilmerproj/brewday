import json
import textwrap

from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields


__all__ = ['Yeast']


class Yeast(object):
    """
    A representation of a type of Yeast as added to a Recipe.
    """

    def __init__(self, name,
                 percent_attenuation=0.75):
        """
        Percent Attenuation - The percentage the yeast is expected to
            attenuate the sugar in the beer to create alcohol.
        """
        self.name = name
        self.percent_attenuation = validate_percentage(percent_attenuation)

    def __str__(self):
        return "{0}, attenuation {1}%".format(self.name.capitalize(),
                                              self.percent_attenuation)

    def __repr__(self):
        out = "{0}('{1}'".format(type(self).__name__, self.name)
        if self.percent_attenuation:
            out = "{0}, percent_attenuation={1}".format(
                out, self.percent_attenuation)
        out = "{0})".format(out)
        return out

    def to_dict(self):
        return {'name': self.name,
                'data': {
                    'percent_attenuation': self.percent_attenuation,
                },
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, yeast_data):
        required_fields = [('name', str),
                           ]
        optional_fields = [('percent_attenuation', float),
                           ]
        validate_required_fields(yeast_data, required_fields)
        validate_optional_fields(yeast_data, optional_fields)

    def format(self):
        msg = textwrap.dedent("""\
                {name} Yeast
                -----------------------------------
                Attenuation:  {data[percent_attenuation]} %""".format(
            **self.to_dict()))
        return msg
