from django.db import models



class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    class Meta:
        # 有该属性的Model类不会完成数据库迁移产生一张表 - 基表
        abstract = True

class Book(BaseModel):
    book_title = models.CharField(max_length=64, verbose_name="书名")
    book_cover = models.ImageField(upload_to='book_cover/', verbose_name='书籍封面', null=True, blank=True,default='book_cover/默认封面.jpg')
    price = models.DecimalField(default=0, max_digits=8, decimal_places=1, verbose_name="售价")
    is_free = models.BooleanField(default=False, verbose_name="限时免费")
    book_brief = models.TextField(verbose_name="简介", null=True,blank=True,default='小说为c享用户自主上传,没有简介')
    is_show = models.BooleanField(verbose_name="是否显示", default=True)
    book_preview = models.TextField(verbose_name='书籍导读', null=True, blank=True)
    book_audio = models.FileField(upload_to='book_audio/', verbose_name='书籍音频', null=True, blank=True)
    book_video = models.FileField(upload_to='book_video/', verbose_name='书籍视频', null=True, blank=True)
    #  ==<外键关联>:[多对多]==
    author = models.ManyToManyField(to="Author")
    book_rack = models.ManyToManyField(to="BookRack", related_name='book',blank=True)
    book_category = models.ForeignKey(to='BookCategory', related_name='books', db_constraint=False,on_delete=models.SET_DEFAULT, default=1)
    ballot=models.IntegerField(verbose_name='得票', null=True, blank=True,default=0)
    class Meta:
        db_table = "CX_Book"
        verbose_name_plural = "图书"

    def __str__(self):
        return self.book_title

    @property
    def authors(self):
        authors = []
        for author in self.author.all():
            authors.append(author.author_name)
        authors = ' | '.join(authors)
        return authors

def get_file_path(book_name, section_name):
    return 'section_content/%s/%s' % (book_name, section_name)

class BookContent(BaseModel):
    section=models.CharField(max_length=256,verbose_name='章节名')
    section_content=models.FileField(upload_to=get_file_path,null=True,blank=True)
    book=models.ForeignKey(to='Book',related_name='sections',db_constraint=False,on_delete=models.CASCADE,verbose_name='所属书名')
    word_number=models.IntegerField(null=True,blank=True,verbose_name='章节字数')
    comment_num = models.IntegerField(default=0)
    class Meta:
        db_table = "CX_BookContent"
        verbose_name_plural = "章节"

    def __str__(self):
        return self.section


class BookCategory(BaseModel):
    # def __init__(self,book_category_id):
    #     self.book_category_id=book_category_id
    #     super().__init__()
    category_name = models.CharField(max_length=32)
    class Meta:
        db_table = "CX_BookCategory"
        verbose_name_plural = "书籍分类"

    # @property
    # def books(self):
    #     book_query=Book.objects.filter(book_category_id=self.book_category_id).all()
    #     return book_query

    def __str__(self):
        return self.category_name




class Author(BaseModel):
    author_name = models.CharField(max_length=32, verbose_name="作者")
    author_age = models.IntegerField(null=True, blank=True, verbose_name="年龄")

    class Meta:
        db_table = "CX_Author"
        verbose_name_plural = "作者"

    def __str__(self):
        return self.author_name







class BookRack(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="加入书架时间")

    class Meta:
        db_table = "CX_BookRack"
        verbose_name_plural = "书架"

    def __str__(self):
        return "[%s]的书架" % self.user

