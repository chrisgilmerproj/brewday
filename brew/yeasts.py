# -*- coding: utf-8 -*-
import json
import sys
import textwrap

from .validators import validate_optional_fields
from .validators import validate_percentage
from .validators import validate_required_fields

__all__ = [u'Yeast']


class Yeast(object):
    """
    A representation of a type of Yeast as added to a Recipe.
    """

    def __init__(self, name,
                 percent_attenuation=0.75):
        """
        :param float percent_attenuation: The percentage the yeast is expected to attenuate the sugar in the yeast to create alcohol
        :raises Exception: If percent_attenuation is not provided
        """  # noqa
        self.name = name
        if percent_attenuation is None:
            raise Exception(u"Must provide percent attenuation")
        self.percent_attenuation = validate_percentage(percent_attenuation)

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return u"{0}, attenuation {1:0.1%}".format(self.name.capitalize(),
                                                   self.percent_attenuation)

    def __repr__(self):
        out = u"{0}('{1}'".format(type(self).__name__, self.name)
        if self.percent_attenuation:
            out = u"{0}, percent_attenuation={1}".format(
                out, self.percent_attenuation)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.name == other.name) and \
           (self.percent_attenuation == other.percent_attenuation):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {u'name': self.name,
                u'data': {
                    u'percent_attenuation': self.percent_attenuation,
                },
                }

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, yeast_data):
        required_fields = [(u'name', str),
                           ]
        optional_fields = [(u'percent_attenuation', float),
                           ]
        validate_required_fields(yeast_data, required_fields)
        validate_optional_fields(yeast_data, optional_fields)

    def format(self):
        msg = textwrap.dedent(u"""\
                {name} Yeast
                -----------------------------------
                Attenuation:  {data[percent_attenuation]:0.1%}""".format(
            **self.to_dict()))
        return msg
