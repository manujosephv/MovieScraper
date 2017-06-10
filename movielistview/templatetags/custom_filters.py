from django import template
# from django.utils.encoding import smart_str
# from movielistview.unicode_to_ascii import unicode_to_ascii

register = template.Library()

@register.filter(name='get_no_of_stars')
def get_no_of_stars(value):
    if value is None:
        return 0
    else:
        return (round(float(value)/float(2)))


@register.filter(name='encode_utf')
def encode_utf(value):
	# print(value[0])
	# print(value.encode('ascii','ignore'))
	# print "haha"
	ret_str = (value.replace('[u"','')
				.replace("[u'","")
				.replace("u'","")
				.replace('u"','')
				.replace("'","")
				.replace('"','')
				.replace('"]','')
				.replace("']","")
				.replace(']','')
				.replace(r"\s","'s")
				)
	return ret_str
	# return unicode_to_ascii(ret_str.encode('utf-8'))
    # return (value.encode('ascii','ignore'))
    # return map(lambda x: x.encode('ascii','ignore'), value)
    # return str(value[0])

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
    