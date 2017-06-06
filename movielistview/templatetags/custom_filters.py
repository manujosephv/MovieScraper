from django import template



register = template.Library()

@register.filter(name='get_no_of_stars')
def get_no_of_stars(value):
    if value is None:
        return 0
    else:
        return (round(float(value)/float(2)))


@register.filter(name='encode_utf')
def encode_utf(value):
    return (value.encode('ascii','ignore'))

@register.filter(name='key_value')
def key_value(dict, key):
    return dict.get(key, '')

# @register.filter(name='get_yts_link')
# def get_yts_link(value, arg):
#     link = "https://yts.ag/movie/"
#     for part in value.split(" "):
#     	link = link + part + "-"
#     link = link+"-"+arg
#     return link

@register.simple_tag(name='torrentz_link')
def torrentz_link(movie_name, movie_year):
    link = "https://torrentz2.eu/search?f="
    for part in movie_name.split(" "):
    	if part:
    		link = link + part.lower() + "+"
    link = link + movie_year
    return link
@register.simple_tag(name='yts_link')
def yts_link(movie_name):
    return "https://yts.ag/browse-movies/" + movie_name + "/all/all/0/latest"
    