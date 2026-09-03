'''
This file contains the unit tests for the models.py file
'''


from app.models import Blog, Image, Page, Reference


def test_new_page(test_database):
    page = Page(pagetitle='Greenland', pageroute='/photos/greenland')
    test_database.session.add(page)
    test_database.session.commit()
    page_id = page.id

    test_database.session.expunge_all()
    committed_page = test_database.session.get(Page, page_id)

    assert committed_page is not None
    assert committed_page.id == page_id
    assert committed_page.pagetitle == "Greenland"
    assert committed_page.pageroute == "/photos/greenland"
    assert committed_page.__repr__() == (
        f"<Page(id={page_id}, pagetitle=Greenland, pageroute=/photos/greenland)>"
    )


def test_new_image(test_database):
    page = Page(pagetitle='Test Images', pageroute='/photos/test-images')
    image = Image(
        imagelink='https://mylink',
        imagetitle='My Title',
        mediatype='Image',
        pagerow=15,
        pagecolumn=1,
        pages=page,
    )
    test_database.session.add(image)
    test_database.session.commit()
    image_id = image.id
    page_id = page.id

    test_database.session.expunge_all()
    committed_image = test_database.session.get(Image, image_id)

    assert committed_image is not None
    assert committed_image.id == image_id
    assert committed_image.imagelink == "https://mylink"
    assert committed_image.imagetitle == "My Title"
    assert committed_image.mediatype == "Image"
    assert committed_image.pagerow == 15
    assert committed_image.pagecolumn == 1
    assert committed_image.page_id == page_id
    assert committed_image.__repr__() == (
        f"<Image(id={image_id}, imagelink=https://mylink, "
        "imagetitle=My Title, pagerow=15, pagecolumn=1)>"
    )


def test_new_reference(test_database):
    reference = Reference(
        authors='P. Lessner, A. Gurav, R. Hahn,',
        title='MLCC and Tantalum',
        refinfo='J. Combined Dielec.',
        date='2021-09-15',
        reflink='https://mylink',
        reftype='Paper',
    )
    test_database.session.add(reference)
    test_database.session.commit()
    reference_id = reference.id

    test_database.session.expunge_all()
    committed_reference = test_database.session.get(Reference, reference_id)

    assert committed_reference is not None
    assert committed_reference.id == reference_id
    assert committed_reference.authors == "P. Lessner, A. Gurav, R. Hahn,"
    assert committed_reference.title == "MLCC and Tantalum"
    assert committed_reference.refinfo == "J. Combined Dielec."
    assert committed_reference.date == "2021-09-15"
    assert committed_reference.reflink == "https://mylink"
    assert committed_reference.reftype == "Paper"
    assert committed_reference.__repr__() == (
        f"<Reference(id={reference_id}, authors=P. Lessner, A. Gurav, R. Hahn,, "
        "title=MLCC and Tantalum, refinfo=J. Combined Dielec., "
        "reflink=https://mylink, date=2021-09-15, reftype=Paper)>"
    )


def test_new_blog(test_database):
    page_css = (
        '<style type="text/css"> @page { size: 8.5in 11in; margin: 1in }</style>'
    )
    blog = Blog(
        title='My Blog Post',
        body='<p>This is my blog post</p>',
        date='2024-12-28',
        abstract='I hope you read this post.',
        medialink='https://myphoto',
        mediatype='Image',
        pagecss=page_css,
    )
    test_database.session.add(blog)
    test_database.session.commit()
    blog_id = blog.id

    test_database.session.expunge_all()
    committed_blog = test_database.session.get(Blog, blog_id)

    assert committed_blog is not None
    assert committed_blog.id == blog_id
    assert committed_blog.title == "My Blog Post"
    assert committed_blog.body == "<p>This is my blog post</p>"
    assert committed_blog.date == "2024-12-28"
    assert committed_blog.abstract == "I hope you read this post."
    assert committed_blog.medialink == "https://myphoto"
    assert committed_blog.mediatype == "Image"
    assert committed_blog.pagecss == page_css
    assert committed_blog.__repr__() == (
        f"<Blog(id={blog_id}, title=My Blog Post, date=2024-12-28)>"
    )
