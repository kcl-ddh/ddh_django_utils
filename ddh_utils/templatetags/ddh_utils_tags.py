from django import template

from ..utils import PaginationDisplay


register = template.Library()


@register.inclusion_tag('includes/pagination.html')
def display_pagination(qd, page):
    """Includes a template displaying a full pagination listing in the
    context of `page`.

    :param qd: query paramters to base URLs on
    :type qd: `django.http.QueryDict`
    :param page: context page of a set of paginated results
    :type page: `django.core.paginator.Page`
    :rtype: `dict`

    """
    pd = PaginationDisplay(qd)
    return {'data': pd.generate_data(page)}


@register.simple_tag
def add_facet_link(qd, facet, value):
    """Returns a URL with `facet` and its `value` added to the query
    parameters in `qd`.

    :param qd: query paramters to base URLs on
    :type qd: `django.http.QueryDict`pass
    :param facet: name of facet to add
    :type facet: `str`
    :param value: value of facet to add
    :type value: `str`
    :rtype: `str`

    """
    qd = qd.copy()
    qd['page'] = 1
    facets = qd.getlist('selected_facets', [])
    facet_value = '{0}_exact:{1}'.format(facet, value.encode('utf-8'))
    if facet_value not in facets:
        facets.append(facet_value)
        qd.setlist('selected_facets', facets)
    return '?{0}'.format(qd.urlencode())


@register.simple_tag
def remove_facet_link(qd, facet):
    """Returns a URL with `facet` removed from the query parameters in
    `qd`.

    :param qd: query paramters to base URLs on
    :type qd: `django.http.QueryDict`pass
    :param facet: facet (name and value combined) to remove
    :type facet: `str`
    :rtype: `str`

    """
    qd = qd.copy()
    qd['page'] = 1
    facets = qd.getlist('selected_facets', [])
    try:
        facets.remove(facet)
    except ValueError:
        pass
    return '?{0}'.format(qd.urlencode())
