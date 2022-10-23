from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author_User = models.OneToOneField(User, on_delete=models.CASCADE)
    Author_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author_User}'


    def update_rating(self):
        post_rating = self.post_set.aggregate(sum_rating=Sum('rating'))
        p_rat = 0
        p_rat += post_rating.get('sum_rating')

        comm_rating = self.author_User.comment_set.aggregate(sum_comm=Sum('rating'))
        c_rat = 0
        c_rat += comm_rating.get('sum_comm')

        pc_rat = 0
        post_com_rating = self.post_set.all()
        for i in post_com_rating:
            pc_rat += i.comment_set.aggregate(sum_comm=Sum('rating')).get('sum_comm')

        '''self.post.comment_set.aggregate(sum_rating=Sum('rating'))'''



        self.Author_rating = p_rat * 3 + c_rat + pc_rat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribes = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    autor = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )

    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOISES, default=ARTICLE)
    date_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.date_time.strftime("%Y-%m-%d  %H.%M")}: {self. heading}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class PostCategory(models.Model):
    categoryT = models.ForeignKey(Category, on_delete=models.CASCADE)
    postT = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_coment = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




