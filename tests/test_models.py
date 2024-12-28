'''
This file contains the unit tests for the models.py file
'''


from app.models import Page, Image, Reference, Blog


def test_new_page():
    page = Page(id=42, pagetitle='Greenland', pageroute='/photos/greenland')
    assert page.id == 42
    assert page.pagetitle == "Greenland"
    assert page.pageroute == "/photos/greenland"
    assert page.__repr__() == "<Page(id=42, pagetitle=Greenland, pageroute=/photos/greenland)>"


def test_new_image():
    image = Image(id=42, imagelink='https://mylink', imagetitle='My Title',
                  pagerow=15, pagecolumn=1)
    assert image.id == 42
    assert image.imagelink == "https://mylink"
    assert image.imagetitle == "My Title"
    assert image.pagerow == 15
    assert image.pagecolumn == 1
    assert image.__repr__() == "<Image(id=42, imagelink=https://mylink, imagetitle=My Title, pagerow=15, pagecolumn=1)>"


def test_new_reference():
    reference = Reference(id=42, authors='P. Lessner, A. Gurav, R. Hahn,',
                          title='MLCC and Tantalum', refinfo='J. Combined Dielec.',
                          date='2021-09-15', reflink='https://mylink', reftype='Paper')
    assert reference.id == 42
    assert reference.authors == "P. Lessner, A. Gurav, R. Hahn,"
    assert reference.title == "MLCC and Tantalum"
    assert reference.refinfo == "J. Combined Dielec."
    assert reference.date == "2021-09-15"
    assert reference.reflink == "https://mylink"
    assert reference.reftype == "Paper"
    assert reference.__repr__() == "<Reference(id=42, authors=P. Lessner, A. Gurav, R. Hahn,, title=MLCC and Tantalum, refinfo=J. Combined Dielec., reflink=https://mylink, date=2021-09-15, reftype=Paper)>"


def test_new_blog():
    blog = Blog(id=42, title='My Blog Post', body='<p>This is my blog post</p>',
                date='2024-12-28', abstract='I hope you read this post.',
                medialink='https://myphoto', mediatype='Image', pagecss='<style type="text/css"> @page { size: 8.5in 11in; margin: 1in }</style>')
    assert blog.id == 42
    assert blog.title == "My Blog Post"
    assert blog.body == "<p>This is my blog post</p>"
    assert blog.date == "2024-12-28"
    assert blog.abstract == "I hope you read this post."
    assert blog.medialink == "https://myphoto"
    assert blog.mediatype == "Image"
    assert blog.pagecss == '<style type="text/css"> @page { size: 8.5in 11in; margin: 1in }</style>'
    assert blog.__repr__() == "<Blog(id=42, title=My Blog Post, date=2024-12-28)>"