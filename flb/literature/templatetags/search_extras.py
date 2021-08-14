from django import template

register = template.Library()


# Custom tag to get the correct url for search filters when adding a filter
@register.simple_tag(takes_context=True)
def add_to_url(context, k, v):
    r = context["request"]
    g = r.GET.copy()
    g.update({k: v})
    return r.path + "?" + g.urlencode()


# Custom tag to get the correct url for search filters when adding a filter
@register.simple_tag(takes_context=True)
def add_replace_to_url(context, k, v):
    r = context["request"]
    g = r.GET.copy()
    if g.__contains__(k):
        g.pop(k)
    g.update({k: v})
    return r.path + "?" + g.urlencode()


# Custom tag to get the correct url for search filters when removing a filter
@register.simple_tag(takes_context=True)
def del_from_url(context, k):
    r = context["request"]
    g = r.GET.copy()
    if g.__contains__(k):
        g.pop(k)
    if g.urlencode() == "":
        return r.path
    else:
        return r.path + "?" + g.urlencode()
