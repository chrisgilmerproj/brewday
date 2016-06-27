import string
import textwrap

from .validators import validate_percentage


class Yeast(object):

    def __init__(self, name,
                 percent_attenuation=0.75):
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

    def format(self):
        msg = textwrap.dedent("""\
                {0} Yeast
                {1}
                Attenuation:  {2} %""".format(
                    string.capwords(self.name),
                    '-' * (len(self.name) + 5),
                    self.percent_attenuation))
        return msg
