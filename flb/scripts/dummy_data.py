from random import choice, randint, sample

from faker import Faker
from taggit.models import Tag

from flb.literature.models import Article, Author, Book, Issue, Journal
from flb.mainsite.models import Organization
from flb.posts.models import Post

fake = Faker()

journals = [
    "Lappmeisen",
    "Fugler i Troms",
    "Trøndersk Natur",
    "Rallus",
    "Fuglar i Hordaland",
    "Falco",
    "Piplerka",
    "Fugler i Aust-Agder",
    "Fugler i Telemark",
    "Vestfold-Ornitologen",
    "Buskskvetten",
    "Hujon",
    "Kornkråka",
]


def create_tag():
    tag, created = Tag.objects.get_or_create(name=fake.word())


def create_organization():
    org, created = Organization.objects.get_or_create(
        name=fake.company(),
        desc=fake.text(randint(100, 200)),
    )
    print(org.name)
    print(org.desc)


def create_journal(n):
    journal, created = Journal.objects.get_or_create(
        name=n,
        desc=fake.text(randint(100, 500)),
        link=fake.uri(),
        publisher=choice(list(Organization.objects.all())),
    )
    print(journal.name)


def create_issue():
    fake_date = fake.date_this_century()
    issue, created = Issue.objects.get_or_create(
        name=fake_date.strftime("%B") + ", " + fake_date.strftime("%Y"),
        volume=randint(1, 5),
        date=fake_date,
        issn=fake.ean(length=13),
        desc=fake.text(randint(100, 500)),
        link=fake.uri(),
        redactor=choice(list(Author.objects.all())),
        journal=choice(list(Journal.objects.all())),
    )
    print(issue.name)


def create_article():
    article, created = Article.objects.get_or_create(
        name=fake.text(randint(50, 100)),
        abstract=fake.text(randint(100, 500)),
        text=fake.text(randint(500, 2000)),
        link=fake.uri(),
        issue=choice(list(Issue.objects.all())),
    )
    sample_authors = sample(list(Author.objects.all()), randint(1, 3))
    for author in sample_authors:
        article.authors.add(author)

    sample_tags = sample(list(Tag.objects.all()), randint(1, 5))
    for tag in sample_tags:
        article.tags.add(tag)

    print(article.name)


def create_book():
    book, created = Book.objects.get_or_create(
        name=fake.text(randint(10, 50)),
        desc=fake.text(randint(100, 250)),
        link=fake.uri(),
        date=fake.date_this_century(),
        issn=fake.ean(length=13),
    )
    sample_authors = sample(list(Author.objects.all()), randint(1, 4))
    for author in sample_authors:
        book.authors.add(author)

    sample_tags = sample(list(Tag.objects.all()), randint(1, 5))
    for tag in sample_tags:
        book.tags.add(tag)

    print(book.name)


def create_author():
    author, created = Author.objects.get_or_create(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        org=choice(list(Organization.objects.all())),
    )
    print(author.first_name, author.last_name)


def create_post():
    post, created = Post.objects.get_or_create(
        name=fake.text(randint(10, 50)),
        text=fake.text(randint(100, 500)),
        author=choice(list(Author.objects.all())),
    )
    print(post.name)


def run():
    Article.objects.all().delete()
    Book.objects.all().delete()
    Journal.objects.all().delete()
    Issue.objects.all().delete()
    Author.objects.all().delete()
    Organization.objects.all().delete()
    Post.objects.all().delete()
    Tag.objects.all().delete()

    print("Starting creating organizations=====================================")
    for i in range(50):
        create_organization()

    print("Starting creating tags=====================================")
    for i in range(200):
        create_tag()

    print("Starting creating authors==================================")
    for i in range(500):
        create_author()

    print("Starting creating journals==================================")
    for j in journals:
        create_journal(j)

    print("Starting creating issues==================================")
    for i in range(300):
        create_issue()

    print("Starting creating books==================================")
    for i in range(200):
        create_book()

    print("Starting creating articles==================================")
    for i in range(1000):
        create_article()

    print("Starting creating posts==================================")
    for i in range(200):
        create_post()
