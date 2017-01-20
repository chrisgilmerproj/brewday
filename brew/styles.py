# -*- coding: utf-8 -*-
import json
import sys
import textwrap

from .validators import validate_required_fields

__all__ = [u'Style']


class Style(object):
    """
    A beer style
    """

    def __init__(self,
                 style,
                 category=u'',
                 subcategory=u'',
                 og=None,
                 fg=None,
                 abv=None,
                 ibu=None,
                 color=None):
        """
        :param str category: The style category
        :param str subcategory: The style subcategory
        :param str style: The style name
        :param list(float) og: The lower and upper original gravity
        :param list(float) fg: The lower and upper final gravity
        :param list(float) abv: The lower and upper alcohol by volume
        :param list(float) ibu: The lower and upper IBU
        :param list(float) color: The lower and upper color (in SRM)
        """
        self.category = category
        self.subcategory = subcategory
        self.style = style
        self.og = self._validate_input_list(og, float, u"Original Gravity")
        self.fg = self._validate_input_list(fg, float, u"Final Gravity")
        self.abv = self._validate_input_list(abv, (int, float), u"ABV")
        self.ibu = self._validate_input_list(ibu, (int, float), u"IBU")
        self.color = self._validate_input_list(color, (int, float), u"Color")

    @classmethod
    def _validate_input_list(cls, value_list, value_type, name):
        """
        Private class to validate inputs for class parameters

        :param list value_list: A list of values to validate
        :param str name: The name of the value_list being validated
        """
        if not value_list:
            raise Exception(u"Must provide {}".format(name))
        if not isinstance(value_list, (list, tuple)):
            raise Exception(u"{} must be a list".format(name))
        if len(value_list) != 2:
            raise Exception(u"{} must contain two value_lists".format(name))
        for v in value_list:
            if not isinstance(v, value_type):
                raise Exception(u"{} must be type '{}'".format(name, value_type))  # noqa
        if value_list[0] > value_list[1]:
            raise Exception(u"{} values must be lowest value first".format(name))  # noqa
        return value_list

    def __str__(self):
        if sys.version_info[0] >= 3:
            return self.__unicode__()
        else:
            return self.__unicode__().encode(u'utf8')

    def __unicode__(self):
        return u"{}{} {}".format(self.category, self.subcategory, self.style)

    def __repr__(self):
        out = u"{0}('{1}'".format(type(self).__name__, self.style)
        out = u"{0}, category='{1}'".format(out, self.category)
        out = u"{0}, subcategory='{1}'".format(out, self.subcategory)
        out = u"{0}, og={1}".format(out, self.og)
        out = u"{0}, fg={1}".format(out, self.fg)
        out = u"{0}, abv={1}".format(out, self.abv)
        out = u"{0}, ibu={1}".format(out, self.ibu)
        out = u"{0}, color={1}".format(out, self.color)
        out = u"{0})".format(out)
        return out

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if (self.style == other.style) and \
           (self.category == other.category) and \
           (self.subcategory == other.subcategory) and \
           (self.og == other.og) and \
           (self.fg == other.fg) and \
           (self.abv == other.abv) and \
           (self.ibu == other.ibu) and \
           (self.color == other.color):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def og_matches(self, og):
        """
        Determine if og matches the style

        :param float og: Original Gravity
        :return: True if matches style, otherwise False
        :rtyle: bool
        """
        return (self.og[0] <= og <= self.og[1])

    def og_errors(self, og):
        """
        Return list of errors if og doesn't match the style

        :param float og: Original Gravity
        :return: List
        :rtyle: list
        """
        errors = []
        if og < self.og[0]:
            errors.append(u'OG is below style')
        if og > self.og[1]:
            errors.append(u'OG is above style')
        return errors

    def fg_matches(self, fg):
        """
        Determine if fg matches the style

        :param float fg: Final Gravity
        :return: True if matches style, otherwise False
        :rtyle: bool
        """
        return (self.fg[0] <= fg <= self.fg[1])

    def fg_errors(self, fg):
        """
        Return list of errors if fg doesn't match the style

        :param float fg: Final Gravity
        :return: List
        :rtyle: list
        """
        errors = []
        if fg < self.fg[0]:
            errors.append(u'FG is below style')
        if fg > self.fg[1]:
            errors.append(u'FG is above style')
        return errors

    def abv_matches(self, abv):
        """
        Determine if abv matches the style

        :param float abv: Alcohol by Volume
        :return: True if matches style, otherwise False
        :rtyle: bool
        """
        return (self.abv[0] <= abv <= self.abv[1])

    def abv_errors(self, abv):
        """
        Return list of errors if abv doesn't match the style

        :param float abv: Alcohol by Volume
        :return: List
        :rtyle: list
        """
        errors = []
        if abv < self.abv[0]:
            errors.append(u'ABV is below style')
        if abv > self.abv[1]:
            errors.append(u'ABV is above style')
        return errors

    def ibu_matches(self, ibu):
        """
        Determine if ibu matches the style

        :param float ibu: IBU
        :return: True if matches style, otherwise False
        :rtyle: bool
        """
        return (self.ibu[0] <= ibu <= self.ibu[1])

    def ibu_errors(self, ibu):
        """
        Return list of errors if ibu doesn't match the style

        :param float ibu: IBU
        :return: List
        :rtyle: list
        """
        errors = []
        if ibu < self.ibu[0]:
            errors.append(u'IBU is below style')
        if ibu > self.ibu[1]:
            errors.append(u'IBU is above style')
        return errors

    def color_matches(self, color):
        """
        Determine if color matches the style

        :param float color: Color in SRM
        :return: True if matches style, otherwise False
        :rtyle: bool
        """
        return (self.color[0] <= color <= self.color[1])

    def color_errors(self, color):
        """
        Return list of errors if color doesn't match the style

        :param float color: Color in SRM
        :return: List
        :rtyle: list
        """
        errors = []
        if color < self.color[0]:
            errors.append(u'Color is below style')
        if color > self.color[1]:
            errors.append(u'Color is above style')
        return errors

    def recipe_matches(self, recipe):
        """
        Determine if a recipe matches the style

        :param Recipe recipe: A Recipe object
        :return: True if recipe matches style, otherwise False
        :rtype: bool
        """
        if self.og_matches(recipe.og) and \
           self.fg_matches(recipe.fg) and \
           self.abv_matches(recipe.abv) and \
           self.ibu_matches(recipe.ibu) and \
           self.color_matches(recipe.color):
            return True
        return False

    def recipe_errors(self, recipe):
        """
        Return list errors if the recipe doesn't match the style

        :param Recipe recipe: A Recipe object
        :return: Errors
        :rtype: list
        """
        errors = []
        errors.extend(self.og_errors(recipe.og))
        errors.extend(self.fg_errors(recipe.fg))
        errors.extend(self.abv_errors(recipe.abv))
        errors.extend(self.ibu_errors(recipe.ibu))
        errors.extend(self.color_errors(recipe.color))
        return errors

    def to_dict(self):
        style_dict = {
            u'style': self.style,
            u'category': self.category,
            u'subcategory': self.subcategory,
            u'og': self.og,
            u'fg': self.fg,
            u'abv': self.abv,
            u'ibu': self.ibu,
            u'color': self.color,
        }
        return style_dict

    def to_json(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    @classmethod
    def validate(cls, recipe):
        required_fields = [(u'style', str),
                           (u'category', str),
                           (u'subcategory', str),
                           (u'og', (list, tuple)),
                           (u'fg', (list, tuple)),
                           (u'abv', (list, tuple)),
                           (u'ibu', (list, tuple)),
                           (u'color', (list, tuple)),
                           ]
        validate_required_fields(recipe, required_fields)

    def format(self):
        style_data = self.to_dict()
        kwargs = {}
        kwargs.update(style_data)

        msg = u""
        msg += textwrap.dedent(u"""\
            {category}{subcategory} {style}
            ===================================

            Original Gravity:   {og[0]:0.3f} - {og[1]:0.3f}
            Final Gravity:      {fg[0]:0.3f} - {fg[1]:0.3f}
            ABV:                {abv[0]:0.2%} - {abv[1]:0.2%}
            IBU:                {ibu[0]:0.1f} - {ibu[1]:0.1f}
            Color (SRM):        {color[0]:0.1f} - {color[1]:0.1f}
            """.format(**kwargs))  # noqa
        return msg
