from django.core.paginator import Paginator, Page


class MyPage(Page):

    def get_page_area(self):
        if self.paginator.num_pages <= 7:
            page_area = self.paginator.page_range
        else:
            start = self.number - 3
            end = self.number + 3
            if start < 1:
                end += 1 - start
                start = 1
            if end > self.paginator.num_pages:
                start -= end - self.paginator.num_pages
                end = self.paginator.num_pages
            page_area = range(start, end+1)
        return page_area


class MyPaginator(Paginator):

    def _get_page(self, *args, **kwargs):
        """
        Returns an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return MyPage(*args, **kwargs)
