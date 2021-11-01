from project import db
from project.com.vo.BlogVO import BlogVO
from project.com.vo.LoginVO import LoginVO


class BlogDAO:
    def viewBlog(self):
        BlogList = db.session.query(BlogVO, LoginVO).join(LoginVO,
                                                              BlogVO.BlogFrom_LoginId == LoginVO.loginId).all()

        return BlogList

    def adminReviewBlog(self, BlogVO):
        db.session.merge(BlogVO)
        db.session.commit()

    def userInsertBlog(self, BlogVO):
        db.session.add(BlogVO)
        db.session.commit()

    def userViewBlog(self, BlogVO):
        BlogList = BlogVO.query.filter_by(BlogFrom_LoginId=BlogVO.BlogFrom_LoginId).all()
        return BlogList

    def userDeleteBlog(self, BlogVO):
        BlogId = BlogVO.query.get(BlogVO.BlogId)

        db.session.delete(BlogId)

        db.session.commit()
