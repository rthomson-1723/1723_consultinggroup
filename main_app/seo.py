from django.http import HttpResponse


def robots_txt(request):
    content = """User-agent: *
Allow: /

Sitemap: https://1723consultinggroup.com/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")
